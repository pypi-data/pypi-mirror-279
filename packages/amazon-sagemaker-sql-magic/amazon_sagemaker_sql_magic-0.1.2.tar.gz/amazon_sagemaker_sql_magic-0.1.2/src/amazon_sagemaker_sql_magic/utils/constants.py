# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
class SMSQLMagicConstants:
    COMMAND = "%%sm_sql"
    ARG_METASTORE_ID = "--metastore-id"
    ARG_METASTORE_TYPE = "--metastore-type"
    ARG_CONNECTION_PROPERTIES = "--connection-properties"
    ARG_OUTPUT_DATAFRAME_TYPE = (
        '--output \'{"format": "DATAFRAME", "dataframe_name": <my_dataframe_name>}\''
    )
    ARG_OUTPUT_TYPE = (
        '--output \'{"format": <OUTPUT_FORMAT_TYPE>,  <OUTPUT_FORMAT_ARGUMENT_NAME>: '
        "<OUTPUT_FORMAT_ARGUMENT_VALUE}'"
    )
    ARG_OUTPUT_FORMAT_TYPE = "format"


class SQLDefaultRowLimitConstants:
    DEFAULT_ROW_LIMIT = 1000
    LIMIT_CLAUSES = ["LIMIT", "FETCH", "TOP"]
    SELECT_QUERY_TYPE = "SELECT"


class MetastoreType:
    GLUE_CONNECTION = "GLUE_CONNECTION"


class OutputFormatType:
    """Determines how the sql query output will be processed"""

    DATAFRAME = "DATAFRAME"
    CELL_OUTPUT = "CELL_OUTPUT"
