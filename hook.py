from database_handler import create_connection, execute_query, close_connection,return_data_as_df, return_insert_into_sql_statement_from_df_stg
from lookups import DESTINATION_SCHEMA, InputTypes, ErrorHandling, ETLStep
from logging_handler import show_error_message
from misc_handler import execute_sql_folder
from datetime import datetime
import pandas as pd
import time

def create_etl_checkpoint(db_session):
   schema_destination_table = DESTINATION_SCHEMA.DESTINATION_NAME.value
   # INSEATE OF etl_last_run_date timestamp, it's Date in order to put the last crash date
   query = f"""
         CREATE TABLE IF NOT EXISTS {schema_destination_table}.etl_checkpoint
         (
            etl_last_run_date DATE
         )
         """
   execute_query(db_session, query)

def return_etl_last_updated_date(db_session):
   schema_destination_table = DESTINATION_SCHEMA.DESTINATION_NAME.value
   does_etl_time_exists = False
   query = f"""
      SELECT etl_last_run_date from {schema_destination_table}.etl_checkpoint ORDER BY etl_last_run_date DESC LIMIT 1
   """
   try:
      etl_df = return_data_as_df(file_executor = query, input_type= InputTypes.SQL, db_session= db_session)
      if len(etl_df) == 0:
         return_date = "2012-06-01"
         does_etl_time_exists = False
      else:
         return_date = etl_df['etl_last_run_date'].iloc[0]
         does_etl_time_exists = True
   except Exception as e:
      suffix = str(e)
      error_prefix = ErrorHandling.RETURN_LAST_ETL_DATE_ERROR.value
      show_error_message(error_prefix, suffix)
   finally:
      return return_date, does_etl_time_exists
   
def filter_df_by_etl_date(df, etl_date):
   try:
      filtered_df = df[df['CRASH_DATE'] > etl_date]
      return filtered_df
   except Exception as e:
      suffix = str(e)
      error_prefix = ErrorHandling.HOOK_FILTER_DF_BY_ETL_DATE_ERROR.value
      show_error_message(error_prefix, suffix)

def filter_df_by_etl_date_API(df, etl_date):
   try:
      filtered_df = df[df['crash_date'] > etl_date]
      return filtered_df
   except Exception as e:
      suffix = str(e)
      error_prefix = ErrorHandling.HOOK_FILTER_DF_BY_ETL_DATE_ERROR.value
      show_error_message(error_prefix, suffix)
         
def insert_or_update_etl_checkpoint(db_session,does_etl_time_exists,  etl_date = None):
   schema_destination_table = DESTINATION_SCHEMA.DESTINATION_NAME.value
   if does_etl_time_exists:
      update_query = f"""
   UPDATE {schema_destination_table}.etl_checkpoint SET etl_last_run_date = '{etl_date}'
   """
   else:
      update_query = f"""
   INSERT INTO {schema_destination_table}.etl_checkpoint (etl_last_run_date) VALUES ('{etl_date}')
   """
   try:
      execute_query(db_session= db_session, query=update_query)
   except Exception as e:
      suffix = str(e)
      error_prefix = ErrorHandling.RETURN_INSERT_OR_UPDATE_LAST_ETL_ERROR.value
      show_error_message(error_prefix, suffix)


import time

def execute_hook(df, df2):
    table_name = "All_Accidents"
    table_name2 = "all_injuries"
    sql_folder_path = './SQL_commands'
    etl_step = ETLStep.HOOK
    try:
        start_time = time.time()  
        print("executing hook")
        db_session = create_connection()
        print(f"Time taken for create_connection: {time.time() - start_time} seconds")

        start_time = time.time()
        print("creating etl checkpoint")
        create_etl_checkpoint(db_session=db_session)
        print(f"Time taken for create_etl_checkpoint: {time.time() - start_time} seconds")

        start_time = time.time()
        print("returning last etl updated date")
        return_date, does_etl_time_exists = return_etl_last_updated_date(db_session)
        return_date = pd.to_datetime(return_date)
        print(f"Time taken for return_etl_last_updated_date: {time.time() - start_time} seconds")
        print(return_date)

        start_time = time.time()
        df = filter_df_by_etl_date(df, return_date)
        return_date
        print(f"Time taken for filter_df_by_etl_date: {time.time() - start_time} seconds")

        start_time = time.time()
        df2 = filter_df_by_etl_date_API(df2, return_date)
        print(f"Time taken for filter_df_by_etl_date_API: {time.time() - start_time} seconds")

        start_time = time.time()
        print("Creating insert into staging tables from source1")
        insert_query = return_insert_into_sql_statement_from_df_stg(df, table_name)
        print(f"Time taken for return_insert_into_sql_statement_from_df_stg (source1): {time.time() - start_time} seconds")
        print("inserting data into stg")
        for query in insert_query:
            execute_query(db_session, query)
        print("Success")

        start_time = time.time()
        print("Creating insert into staging tables from source2")
        insert_query2 = return_insert_into_sql_statement_from_df_stg(df2, table_name2)
        print(f"Time taken for return_insert_into_sql_statement_from_df_stg (source2): {time.time() - start_time} seconds")
        print("inserting data into stg")
        for query in insert_query2:
            execute_query(db_session, query)
        print("Success")

        start_time = time.time()
        print("executing sql folder")
        execute_sql_folder(db_session, sql_folder_path, etl_step)
        print(f"Time taken for execute_sql_folder: {time.time() - start_time} seconds")

        print("inserting etl checkpoint")

        start_time = time.time()
        newest_date = df['CRASH_DATE'].max().date()
        insert_or_update_etl_checkpoint(db_session, does_etl_time_exists, newest_date)
        print(f"Time taken for insert_or_update_etl_checkpoint: {time.time() - start_time} seconds")

        print("done")

        close_connection(db_session=db_session)
    except Exception as e:
        suffix = str(e)
        error_prefix = ErrorHandling.EXECUTE_HOOK_ERROR.value
        show_error_message(error_prefix, suffix)




      
