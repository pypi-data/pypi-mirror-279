# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
def unquote_ends(string):
    """
    Remove a single pair of quotes from ends of string.
    :param string:
    :return:
    """
    if not string or len(string) < 2:
        return string
    if (string[0] == "'" and string[-1] == "'") or (string[0] == '"' and string[-1] == '"'):
        return string[1:-1]
    return string
