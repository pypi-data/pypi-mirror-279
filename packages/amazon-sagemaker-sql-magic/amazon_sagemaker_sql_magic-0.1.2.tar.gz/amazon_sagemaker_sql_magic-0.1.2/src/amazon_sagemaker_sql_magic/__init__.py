# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from .sql_magic import SagemakerSqlMagic


def load_ipython_extension(ipython):
    magic = SagemakerSqlMagic(ipython)
    ipython.register_magics(magic)
