""" SQL Helper Functions / Recipes """
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas


def posh_create_or_append(conn, df: pd.DataFrame, table_name: str, cols: tuple | list | set = ()):
    """ Creates a new table or appends, removing duplicated with grouper columns """

    assert isinstance(df, pd.DataFrame), f"df needs to by a pandas dataframe: type{type(df)}-passed"
    assert isinstance(table_name, str), f"""
        table_name must be a string of an existing table or the one to be created: {type(table_name)}-passed """

    with conn.cursor() as cur:

        # use the show tables in SQL to find table of that name; use that to tell if the table exists
        cur.execute(f"SHOW TABLES LIKE '{table_name}'")
        rows = cur.fetchall()
        if len(rows) > 0:
            sql_append_with_drop_duplicates(conn, df, table_name, cols)
        else:
            write_pandas(conn, df, table_name, auto_create_table=True)


def posh_create_or_replace(conn, df: pd.DataFrame, table_name: str):
    """ Creates a new table or replaces """

    assert isinstance(df, pd.DataFrame), f"df needs to by a pandas dataframe: type{type(df)}-passed"

    with conn.cursor() as cur:

        # use the show tables in SQL to find table of that name; use that to tell if the table exists
        cur.execute(f"SHOW TABLES LIKE '{table_name}'")
        rows = cur.fetchall()
        if len(rows) > 0:
            cur.execute(f""" DROP TABLE {table_name}""")

        write_pandas(conn, df, table_name, auto_create_table=True)
        conn.commit()


def check_compatibility(conn, df: pd.DataFrame, table_name: str, map_fudge: dict = {}):
    """ Snowflake Helper Function to Check Dataframe Compatability Before Upload

    In testing had some problems with datatypes when uploading data to Snowflake from a Pandas Dataframe.
    Function runs a series of assert statements to check for compatability.

    Asserts:
    - number of columns in df and snowflake table are the same
    - column names in df match table names in snowflake table
    - data types are mapped; this may not be perfect.

    :arg:
        conn: snowflake connection object
        df: pd.DataFrame: dataframe to be appended
        table_name: str: the table name in Snowflake / the SQL databass
        map_fudge: dict: way of adding data types that may not have been included when the function was written.

    :returns: bool == True if no assertion errors"""

    # get a pd.Series of df data types
    df_types = pd.Series(df.dtypes)

    # Get the column names and data types of the Snowflake table
    with conn.cursor() as cur:
        cur.execute(f"""DESCRIBE {table_name}""")
        result = cur.fetchall()
        cols = [col[0] for col in cur.description]
        original = pd.DataFrame(result, columns=cols).set_index('name')

    # df we want the width, which is no of columns... hence [1]
    # originals df has table cols listed per row... hence [0]
    assert df.shape[1] == original.shape[0], \
        f"Column count in new df: {df.shape[1]} does not match snowflake table: {original.shape[0]}"

    # attempt to map types between Snowflake & Pandas
    # Ref: https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-pandas
    map_snowflake_types = {
        'DATE': ['object'],
        'TIME': ['object'],
        'TIMESTAMP_NTZ': ['datetime64[ns]'],
        'TIMESTAMP_LTZ': ['datetime64[ns]'],
        'TIMESTAMP_TZ': ['datetime64[ns]'],
        'FLOAT': ['float64'],
        'VARCHAR(16777216)': ['object', 'str'],
    }

    # quite possible we are missing dtypes here
    # to avoid having to update hxm-refuel each time we find one, option to append additional types
    map_snowflake_types = map_snowflake_types | map_fudge

    # iterate over each column from the Snowflake Table
    for i in original.index:
        snowflake_type = original.loc[i, 'type']  # snowflake dtype

        assert i in df.columns, \
            f""" Snowflake Table Col {i} missing from dataframe """
        assert snowflake_type in map_snowflake_types.keys(), \
            f""" Snowflake type {snowflake_type} missing from snowflake-to-pandas map. 
            Doesn't necessarily mean something wrong, but update the map to continue. """
        assert df_types[i] in map_snowflake_types[snowflake_type], \
            f""" For col: {i} df has type {df_types[i]}. Snowflake table type {snowflake_type}; 
            this Snowflake type should map to pd types {map_snowflake_types[snowflake_type]}"""

    return True


def sql_append_with_drop_duplicates(
        conn,
        df: pd.DataFrame,
        table_name: str,
        cols: list | set | tuple,
        delete_stage: bool = True,
        run_check_compatability: bool = True):
    """ Append to Snowflake Table but Dropping Duplicates

    Hat tip to Jaco, because this was basically his idea so get the data in via a staging area.
    What we want is an equivalent to df.groupby(cols).last() but in Snowflake, which has weird indexing.
    Approach is to upload to staging table, find duplicates by column-group and remove from the original table,
    then append the new dataframe.

    """

    assert type(cols) in (list, set, tuple), f"cols must be type list|set|tuple but type {cols}-passed"

    if run_check_compatability:
        assert check_compatibility(conn, df, table_name)

    # setup context handler for cursor object
    with conn.cursor() as cur:

        # create staging table & append dataframe
        # in testing trying to create or replace within write_pandas was very hit & miss
        cur.execute(f"""CREATE OR REPLACE TABLE {table_name}_STAGE LIKE {table_name}""")
        write_pandas(conn, df, f"{table_name}_STAGE")  # alternative method that doesn't use engine

        # groupby and delete from original query
        query_delete = f"""
            DELETE FROM {table_name}
            WHERE ({", ".join(f'"{col}"' for col in cols)})
            IN (SELECT {", ".join(f'"{col}"' for col in cols)} FROM {table_name}_STAGE)
            """

        # run delete query & insert staging table into original
        cur.execute(query_delete)
        cur.execute(f"""INSERT INTO {table_name} SELECT * FROM {table_name}_STAGE""")

        # optional to drop the staging table from the database
        if delete_stage:
            cur.execute(f""" DROP TABLE {table_name}_STAGE""")

        conn.commit()  # commit changes
        return True
