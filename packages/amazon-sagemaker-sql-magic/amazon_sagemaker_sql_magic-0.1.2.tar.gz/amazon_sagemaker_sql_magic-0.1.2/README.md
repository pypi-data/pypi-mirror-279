# SageMaker SQL Magic Extension

This is a notebook extension provided by AWS SageMaker Studio team to run SQL queries inside SageMaker Jupyter notebooks. Currently, it supports running SQL on Redshift, Snowflake, and Athena.

## Usage
Introduces the `%%sm_sql` and `%sm_sql_manage` ipython magic commands to run SQL queries inside SageMaker Jupyter notebooks.
### Install
```buildoutcfg
pip install amazon-sagemaker-sql-magic
```
### Register the magic command:
```buildoutcfg
%load_ext amazon_sagemaker_sql_magic
```
### Show help content for `%%sm_sql`:
```buildoutcfg
%%sm_sql?
```
```buildoutcfg
Docstring:
::

  %sm_sql [--metastore-id METASTORE_ID] [--metastore-type METASTORE_TYPE]
              [--query-parameters QUERY_PARAMETERS]
              [--connection-properties CONNECTION_PROPERTIES]
              [--connection-name CONNECTION_NAME] [-df DATAFRAME]

Cell magic command to run SQL queries inside SageMaker Jupyter notebooks.

Format:
    %%sm_sql --metastore-id METASTORE_ID --metastore-type METASTORE_TYPE --query-parameters QUERY_PARAMETERS --connection-properties CONNECTION_PROPERTIES --connection-name CONNECTION_NAME -df, --dataframe DATAFRAME

Examples:
     # How to use '--metastore-id' and '--metastore-type'
     %%sm_sql --metastore-id my_glue_conn --metastore-type GLUE_CONNECTION
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

options:
  --metastore-id METASTORE_ID
                        Defines the metastore entity holding data-source
                        connection parameters e.g. a Glue connection name.
                        Support available for Glue connection.
  --metastore-type METASTORE_TYPE
                        Type of metastore to use for connecting to data-
                        source. Supported value(s): 'GLUE_CONNECTION'
  --query-parameters QUERY_PARAMETERS
                        SQL Query parameters as a dictionary encapsulator. See
                        examples above on how to use.
  --connection-properties CONNECTION_PROPERTIES
                        Data-source connection properties as a dictionary
                        encapsulator.See examples above on how to use.
  --connection-name CONNECTION_NAME
                        Name of the Glue connection to be re-used.
  -df DATAFRAME, --dataframe DATAFRAME
                        The name of pandas dataframe where the query results
                        will be stored
```

### Show help content for `%sm_sql_manage`:
```buildoutcfg
%sm_sql_manage?
```
```buildoutcfg
Docstring:
::

  %sm_sql_manage [--set-connection-reuse SET_CONNECTION_REUSE]
                     [--list-cached-connections] [--clear-cached-connections]

Line magic command to manage SQL connections inside SageMaker Jupyter notebooks.

Format:
  %sm_sql_manage --set-connection-reuse True/False --list-cached-connections --clear-cached-connections

options:
  --set-connection-reuse SET_CONNECTION_REUSE
                        Set if connection should be reused. Example use:
                        %sm_sql_manage --set-connection-reuse True
  --list-cached-connections
                        List the cached connections. Example use:
                        %sm_sql_manage --list-cached-connections
  --clear-cached-connections
                        Clear all cached connections. Example use:
                        %sm_sql_manage --clear-cached-connections
```

### Examples on how to use `%%sm_sql`
1. Connect to a data-source using custom connection properties and fetch data from a table. 
```buildoutcfg
%%sm_sql --connection-properties '{"connection_type": "SNOWFLAKE", "aws_secret_arn":"arn:aws:secretsmanager:us-west-2:123456789012:secret:my-snowflake-secret-123"}'
SELECT * FROM my_db.my_schema.my_table
```

2. Connect to a data-source using a Glue connection and fetch data from a table.  
```buildoutcfg
%%sm_sql --metastore-id my_glue_conn --metastore-type GLUE_CONNECTION
SELECT * FROM my_db.my_schema.my_table
```

3. Connect to a data-source to fetch data from a table and save results into a pandas dataframe. 
```buildoutcfg
%%sm_sql --metastore-id my_glue_conn --metastore-type GLUE_CONNECTION --dataframe my_df
SELECT * FROM my_db.my_schema.my_table
```

4. Connect to a data-source to fetch data from a table using a parameterized SQL query. 
```buildoutcfg
%%sm_sql --metastore-id my_glue_conn --metastore-type GLUE_CONNECTION --query-parameters '{"parameters":("John Smith")}'
UPDATE my_db.my_schema.my_table SET name = (%s);
```
## License

This library is licensed under the Apache 2.0 License. See the LICENSE file.