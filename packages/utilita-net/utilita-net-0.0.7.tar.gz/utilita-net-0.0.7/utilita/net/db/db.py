from sqlalchemy.dialects import postgresql as pgcmd
import sqlalchemy as sa

def records_to_sql(records: iter, con: sa.engine, table: str, schema: str, upsert: bool=False, index_elements: list=None, chunksize=5000) -> bool:
    """ Inserts records into a table. Allows for upserts. This only works on postgresql for now.
    
    Params:
        records (iterator): a list of records in the form of [{col1=val1, col2=val2, col3=val3}]
        con (sqlalchemy engine): a sqlalchemy engine connection
        table (str): destination table name
        schema (str): destination schema name
        upsert (bool): whether to upsert the data. uses postgres dialect ON CONFLICT DO UPDATE
        index_elements (list): a list of column names to match the on conflict statement
        chunksize (int): chunk size to insert on

    Returns:
        True if import was successful
    
    """
    metadata = sa.MetaData()
    table_info = sa.Table(table, metadata, autoload_with=con, schema=schema)
    records = iter(records) # in case the iter is a list.

    with con.begin() as conn:
        has_more_data = True
        total_rows = 0
        while has_more_data:
            records_to_insert = []

            for i in range(chunksize):
                try:
                    records_to_insert.append(next(records))
                    total_rows += 1

                except StopIteration:
                    has_more_data = False
                    break

            if len(records_to_insert) > 0:
                insert_query = pgcmd.insert(table_info).values(records_to_insert)
                del(records_to_insert)
                
                if upsert:
                        if index_elements is None or len(index_elements) == 0:
                                raise ValueError('No index_elements defined for the on conflict statement. You must define what columns the on conflict will hit.')
                        insert_query = insert_query.on_conflict_do_update(
                        index_elements=index_elements,
                        set_={**insert_query.excluded}
                        )
                try:
                    conn.execute(insert_query)
                    print(f'Inserted {total_rows} rows' + (' so far..' if has_more_data else '.'))
                except sa.exc.SQLAlchemyError as e:
                    str_e = str(e)[:2000] + ' <<output truncated>>'
                    raise sa.exc.SQLAlchemyError('got sqlalchemy exception: ' + str_e) from None

    return True

def df_to_sql(df: object, *args, **kwargs):
    """ Wrapper function for records_to_sql(), however accepting a dataframe instead of a records iterator

        Params:
            df (pandas.DataFrame): a DataFrame object
            con (sqlalchemy engine): a sqlalchemy engine connection
            table (str): destination table name
            schema (str): destination schema name
            upsert (bool): upserts the data. uses postgres dialect ON CONFLICT DO UPDATE
            index_elements (list): a list of column names to match the on conflict statement
            chunksize (int): chunk size to insert on

        Returns:
            True if import was successful
    """
    try:
        import pandas as pd
        records = (row.to_dict() for index, row in df.iterrows())
        return records_to_sql(records=records, *args, **kwargs)
    except ImportError:
            raise ImportError('Pandas is not installed or could not be imported.')