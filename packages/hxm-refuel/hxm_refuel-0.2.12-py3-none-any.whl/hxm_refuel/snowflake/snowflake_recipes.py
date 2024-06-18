import pandas as pd
from snowflake.connector.pandas_tools import write_pandas


def snowflake_create_or_replace(df, conn, table_name: str = "TEST", schema: str = "SNOWBERG"):
    """ Simple Function to Create New or Replace Existing Table in Snowflake

    Careful! Replacing an existing table will delete the old version and lose all original data

    INPUTS:
        df: pd.DataFrame
        conn: snowflake connect object; best to use our snowflake_connect method to create it
        table_name: str: name required in snowflake
        schema [optional]: can provide the schema in snowflake if it wasn't part of the connection object

    """

    assert isinstance(table_name, str), f"table_name must be type string: type {type(table_name)} provided"
    assert isinstance(df, pd.DataFrame), f"""
        Can only create or replace dataframes, for {table_name}: type{type(df)}-passed """

    with conn.cursor() as cur:

        # use the show tables in SQL to find table of that name; use that to tell if the table exists
        cur.execute(f"SHOW TABLES LIKE '{table_name}'")
        rows = cur.fetchall()
        if len(rows) > 0:
            cur.execute(f""" DROP TABLE {table_name}""")

        write_pandas(conn, df, table_name, auto_create_table=True)
        conn.commit()
        print(f"{table_name} pushed to Snowflake")


if __name__ == "__main__":
    print("Foo, Bar, Baz")
