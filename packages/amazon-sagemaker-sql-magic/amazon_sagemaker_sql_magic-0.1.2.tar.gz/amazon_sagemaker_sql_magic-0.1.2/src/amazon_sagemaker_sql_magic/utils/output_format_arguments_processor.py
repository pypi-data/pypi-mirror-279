# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""OutputArgumentsProcessor module provides classes which Determine how to handle sql query execution output."""

from abc import abstractmethod

import keyword
import pandas as pd

from IPython.core.display_functions import display
from IPython.core.error import UsageError
from amazon_sagemaker_sql_magic.utils.constants import SMSQLMagicConstants, OutputFormatType


class OutputArgumentsProcessor:
    """Determines how to handle sql query execution output."""

    subclasses = {}

    @classmethod
    def register_subclass(cls, output_format_type):
        """Used by child classes to register the output formats that they can handle

        :param output_format_type:
        :return:
        """

        def decorator(subclass):
            cls.subclasses[output_format_type] = subclass
            return subclass

        return decorator

    @classmethod
    def create(cls, output):
        """Creates appropriate outputFormat subclass

        :param output:
        :return:
        """

        try:
            output_format_type = output["format"].upper()
        except KeyError:
            raise UsageError(
                f"Missing format in output. Provide output as {SMSQLMagicConstants.ARG_OUTPUT_TYPE}"
            )
        if output_format_type not in cls.subclasses:
            raise UsageError(
                f"Unsupported output format: {output_format_type}. "
                f"Supported output formats are: {OutputFormatType.DATAFRAME} and {OutputFormatType.CELL_OUTPUT}"
            )

        return cls.subclasses[output_format_type](output)

    @abstractmethod
    def process(self, shell, sql_execution_response):
        """Method to process results in the given output format type with the given output format arguments

        :param shell: Python shell to set dataframe variable with results of the query
        :param result: Results of the user query
        """
        raise NotImplementedError()

    @staticmethod
    def convert_response_to_dataframe(sql_execution_response):
        """Converts SQL execution response to a dataframe

        :param sql_execution_response:
        :return:
        """
        # Extract column names from column metadata
        column_names = [
            columnMetadataEntry.name
            for columnMetadataEntry in sql_execution_response.column_metadata
        ]

        # Create a pandas DataFrame with column names and data
        df = pd.DataFrame(sql_execution_response.data, columns=column_names)
        return df


@OutputArgumentsProcessor.register_subclass("DATAFRAME")
class DataFrameOutputArgumentsProcessor(OutputArgumentsProcessor):
    """Stores SQL query result in user-specified dataframe"""

    @staticmethod
    def is_valid_variable_name(name):
        """Is variable name valid?

        :param name:
        :return:
        """
        return name.isidentifier() and not keyword.iskeyword(name)

    def __init__(self, output):
        try:
            self.dataframe_name = output["dataframe_name"]
            self.validate_output_arguments()
        except KeyError:
            raise UsageError(
                f"dataframe_name is required. Provide output config as {SMSQLMagicConstants.ARG_OUTPUT_DATAFRAME_TYPE}"
            )

    def validate_output_arguments(self):
        """Determine if arguments are valid.

        :return:
        """
        if not self.is_valid_variable_name(self.dataframe_name):
            raise UsageError("Dataframe name must be a valid python identifier")

    def process(self, shell, sql_execution_response):
        """Stores sql execution result in dataframe.

        :param shell:
        :param sql_execution_response:
        :return:
        """
        df = self.convert_response_to_dataframe(sql_execution_response)

        if self.dataframe_name is not None:
            shell.user_ns.update({self.dataframe_name: df})
            print(f"Saved results to {self.dataframe_name}")
        else:
            print("Could not determine dataframe to store results in. Displaying instead.")
            display(df)
            del df


@OutputArgumentsProcessor.register_subclass("CELL_OUTPUT")
class CellOutputArgumentsProcessor(OutputArgumentsProcessor):
    """Displays SQL Query result as cell output"""

    def __init__(self, output):
        # CELL_OUTPUT does not take any arguments
        pass

    def process(self, shell, sql_execution_response):
        """Displays sql execution result as dataframe.

        :param shell:
        :param sql_execution_response:
        :return:
        """
        df = self.convert_response_to_dataframe(sql_execution_response)
        display(df)
        del df
