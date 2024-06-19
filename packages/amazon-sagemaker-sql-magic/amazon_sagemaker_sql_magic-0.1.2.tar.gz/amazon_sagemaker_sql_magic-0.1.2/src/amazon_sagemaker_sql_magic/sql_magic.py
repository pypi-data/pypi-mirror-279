# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import ast
import logging
import json
import sqlparse

from IPython.core.error import UsageError
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magic_arguments import magic_arguments, argument, parse_argstring
from amazon_sagemaker_sql_execution.exceptions import CredentialsExpiredError
from amazon_sagemaker_sql_execution.models.sql_execution import SQLExecutionRequest
from amazon_sagemaker_sql_execution.utils.sql_connection_factory import SQLConnectionFactory

from amazon_sagemaker_sql_execution.connection_pool import ConnectionPool
from aws_embedded_metrics import MetricsContext
from amazon_sagemaker_sql_execution.utils.metrics.service_metrics import (
    add_metrics,
    create_metrics_context,
)

from .exceptions import MissingParametersError
from .utils.output_format_arguments_processor import OutputArgumentsProcessor
from .utils.string_utils import unquote_ends
from .utils.constants import SMSQLMagicConstants
from .utils.constants import SQLDefaultRowLimitConstants


@magics_class
class SagemakerSqlMagic(Magics):
    def __init__(self, shell=None, **kwargs):
        super().__init__(shell, **kwargs)
        self.reuse_connection: bool = True
        self.connection_pool = ConnectionPool()
        self.metrics_context = create_metrics_context()

    @add_metrics("sm_sql_manage")
    @line_magic
    @magic_arguments()
    @argument(
        "--set-connection-reuse",
        type=str,
        help="Set if connection should be reused. Example use: %%sm_sql_manage --set-connection-reuse True",
    )
    @argument(
        "--list-cached-connections",
        action="store_true",
        help="List the cached connections. Example use: %%sm_sql_manage --list-cached-connections",
    )
    @argument(
        "--clear-cached-connections",
        action="store_true",
        help="Clear all cached connections. Example use: %%sm_sql_manage --clear-cached-connections",
    )
    def sm_sql_manage(self, line):
        """
        Line magic command to manage SQL connections inside SageMaker Jupyter notebooks.

        Format:
          %sm_sql_manage --set-connection-reuse True/False --list-cached-connections --clear-cached-connections
        """
        # NOTE: modifying the above doc-string is a customer facing change since it is automatically picked up by
        # `%sm_sql_manage?` command. Please be careful before modifying it.
        args = parse_argstring(self.sm_sql_manage, line)
        if args is None:
            raise MissingParametersError("Command to be executed must be provided.")

        if args.list_cached_connections:
            cached_connections = self.connection_pool.list_connections()
            self.metrics_context.set_property("ListCachedConnections", 1)

            try:
                # Pretty-print on as best-effort case
                print(json.dumps(json.loads(cached_connections), indent=4))
            except Exception:
                print(cached_connections)

        if args.clear_cached_connections:
            self.connection_pool.close()
            self.metrics_context.set_property("ClearCachedConnections", 1)

        if args.set_connection_reuse:
            self.reuse_connection = args.set_connection_reuse.lower() == "true"
            self.metrics_context.set_property("SetConnectionReuse", self.reuse_connection)

    @add_metrics("sm_sql")
    @cell_magic
    @magic_arguments()
    @argument(
        "--metastore-id",
        type=str,
        default="",
        help="Defines the metastore entity holding data-source connection parameters e.g. a Glue connection name. "
        "Support available for Glue connection.",
    )
    @argument(
        "--metastore-type",
        default="",
        type=str,
        help="Type of metastore to use for connecting to data-source. Supported value(s): 'GLUE_CONNECTION'",
    )
    @argument(
        "--query-parameters",
        type=str,
        help="SQL Query parameters as a dictionary encapsulator. See examples above on how to use.",
    )
    @argument(
        "--connection-properties",
        type=str,
        default="{}",
        help="Data-source connection properties as a dictionary encapsulator.See examples above on how to use.",
    )
    @argument("--connection-name", type=str, help="Name of the Glue connection to be re-used.")
    @argument(
        "--output",
        type=str,
        default='{"format":"CELL_OUTPUT"}',
        help="Specify where to store output of SQL query execution. Available options are: \n"
        '[Default]\'{"format":"CELL_OUTPUT"}\' : Displays output in the cell\n'
        '\'{"format": "DATAFRAME", "dataframe_name": "my_dataframe_name"} : Store results in a pandas dataframe.',
    )
    @argument(
        "--apply-default-row-limit",
        type=str,
        help=f"Takes True/False. True by default. When True, default row limit of"
        f" {SQLDefaultRowLimitConstants.DEFAULT_ROW_LIMIT} will be "
        f"applied to {SQLDefaultRowLimitConstants.SELECT_QUERY_TYPE} queries. If user provides a LIMIT in the query, "
        f"that will take precedence. "
        f"Caution: Without the limit, response data-size can exceed available instance memory and crash the kernel.",
    )
    def sm_sql(self, line, cell):
        """
        Cell magic command to run SQL queries inside SageMaker Jupyter notebooks.

        Format:
            %%sm_sql --metastore-id METASTORE_ID --metastore-type METASTORE_TYPE --apply-default-row-limit True/False --query-parameters QUERY_PARAMETERS --connection-properties CONNECTION_PROPERTIES --connection-name CONNECTION_NAME --output '{"format": "DATAFRAME", "dataframe_name": "my_dataframe_name"}'

        Examples:
            # How to use '--metastore-id' and '--metastore-type'
            %%sm_sql --metastore-id my_glue_conn --metastore-type GLUE_CONNECTION
            SELECT * FROM my_db.my_schema.my_table

            # How to use '--apply-default-row-limit'
            %%sm_sql --metastore-id my_glue_conn --metastore-type GLUE_CONNECTION --apply-default-row-limit True/False
            SELECT * FROM my_db.my_schema.my_table

            # How to use '--connection-properties'
            %%sm_sql --connection-properties '{"connection_type": "SNOWFLAKE", "aws_secret_arn":"arn:aws:secretsmanager:us-west-2:123456789012:secret:my-snowflake-secret-123"}'
            SELECT * FROM my_db.my_schema.my_table

            # How to use '--query-parameters' with SNOWFLAKE/REDSHIFT as a data-source
            %%sm_sql --metastore-id my_glue_conn --metastore-type GLUE_CONNECTION --query-parameters '{"parameters":("John Smith")}'
            SELECT * FROM my_db.my_schema.my_table WHERE name = (%s);

            # How to use '--query-parameters' with ATHENA as a data-source
            %%sm_sql --metastore-id my_glue_conn --metastore-type GLUE_CONNECTION --query-parameters '{"parameters":{"name_var": "John Smith"}}'
            SELECT * FROM my_db.my_schema.my_table WHERE name = (%(name_var)s);

            # How to use '--output' with output format type DATAFRAME
            %%sm_sql --metastore-id my_glue_conn --metastore-type GLUE_CONNECTION --output '{"format": "DATAFRAME", "dataframe_name": "my_dataframe_name"}'
            SELECT * FROM my_db.my_schema.my_table
        """

        args = parse_argstring(self.sm_sql, line)
        self.add_args_as_metrics_properties(args, self.metrics_context)
        connection_properties = (
            ast.literal_eval(unquote_ends(args.connection_properties))
            if args.connection_properties
            else {}
        )

        query_params = (
            ast.literal_eval(unquote_ends(args.query_parameters)) if args.query_parameters else {}
        )

        output = ast.literal_eval(unquote_ends(args.output))
        self.metrics_context.set_property("OutputFormat", output["format"].upper())
        # Processor creation also validates arguments. Must be created before SQL execution.
        output_arguments_processor = OutputArgumentsProcessor.create(output)

        sql_query = self.extract_sql_query_from_cell(cell, args)

        metastore_id = args.metastore_id
        metastore_type = args.metastore_type

        if (
            not args.connection_name
            and not connection_properties
            and (not metastore_id or not metastore_type)
        ):
            raise UsageError(
                "Missing required arguments. "
                f"Provide name of existing connection or provide connection parameters either as"
                f" {SMSQLMagicConstants.ARG_CONNECTION_PROPERTIES}"
                f" or as {SMSQLMagicConstants.ARG_METASTORE_ID} and {SMSQLMagicConstants.ARG_METASTORE_TYPE}"
            )

        try:
            if self.reuse_connection:
                connection = self.connection_pool.get_or_create_connection(
                    metastore_type=metastore_type,
                    metastore_id=metastore_id,
                    connection_parameters=connection_properties,
                    connection_name=args.connection_name,
                )
            else:
                connection = SQLConnectionFactory.create_connection(
                    metastore_id=metastore_id,
                    metastore_type=metastore_type,
                    connection_parameters=connection_properties,
                )
            self.metrics_context.set_property("ReuseConnection", self.reuse_connection)

            execution_request = SQLExecutionRequest(sql_query, query_params)
            try:
                response = connection.execute(execution_request)
            except CredentialsExpiredError:
                self.connection_pool.close_cached_connection(connection)
                raise CredentialsExpiredError(
                    "Credentials expired. The connection was closed, please rerun the query"
                )

            output_arguments_processor.process(self.shell, response)

            if self.reuse_connection is False:
                connection.close()

        except Exception as e:
            logging.error(f"Error executing SQL query: {cell}\n{e}")
            raise e

    def extract_sql_query_from_cell(self, cell, args):
        """Applies all required transformations on the cell content to determine the SQL query to execute.

        As of now, it:
        1. Applies default limit if needed on SQL query

        :param cell:
        :param args:
        :return:
        """

        # Default limit will be applied to the number of rows fetched when apply_default_row_limit argument is not
        # present or is True
        apply_default_row_limit = (
            True
            if args.apply_default_row_limit is None
            or args.apply_default_row_limit.lower() == "true"
            else False
        )

        if apply_default_row_limit:
            sql_query = self.get_sql_query_with_limit(cell)
        else:
            sql_query = cell

        return sql_query

    # Default limit of 1000 will be applied to SELECT queries when user has not already provided a limiting clause in
    # query
    def get_sql_query_with_limit(self, cell):
        try:
            parsed_query = sqlparse.parse(cell)[0]

            if parsed_query.get_type() == SQLDefaultRowLimitConstants.SELECT_QUERY_TYPE:
                for token in parsed_query:
                    if token.value.upper() in SQLDefaultRowLimitConstants.LIMIT_CLAUSES:
                        return cell
                return (
                    f"SELECT * FROM ({cell}) LIMIT {SQLDefaultRowLimitConstants.DEFAULT_ROW_LIMIT}"
                )

            return cell
        except sqlparse.exceptions.SQLParseError as e:
            logging.error(f"Error parsing SQL query: {cell} with {e}")
            return cell

    def add_args_as_metrics_properties(self, args, context: MetricsContext):
        if args.connection_properties:
            context.set_property("ConnectionPropertiesProvided", 1)
        if args.query_parameters:
            context.set_property("QueryParametersProvided", 1)
        if args.metastore_id:
            context.set_property("MetastoreIdProvided", 1)
        if args.apply_default_row_limit:
            context.set_property("ApplyDefaultRowLimit", args.apply_default_row_limit)
        if args.metastore_type:
            context.set_property("MetastoreType", args.metastore_type)
