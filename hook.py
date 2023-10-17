from database_handler import create_connection, execute_query, close_connection,return_data_as_df
from lookups import DESTINATION_SCHEMA, InputTypes, ErrorHandling
from logging_handler import show_error_message
from misc_handler import execute_sql_folder

def create_etl_checkpoint(db_session):
   schema_destination_table = DESTINATION_SCHEMA.DESTINATION_NAME.value
   # INSEATE OF etl_last_run_date timestamp, it's Date in order to put the last crash date
   query = f"""
         CREATE TABLE IF NOT EXISTS {schema_destination_table}.elt_checkpoint
         (
            etl_last_run_date DATE
         )
         """
   execute_query(db_session, query)

def return_etl_last_updated_date(db_session):
   schema_destination_table = DESTINATION_SCHEMA.DESTINATION_NAME.value
   does_etl_time_exists = False
   query = f""""
      SELECT elt_last_run_date from {schema_destination_table}.etl_checkpoint ORDER BY etl_last_run_date DESC LIMIT 1
   """
   try:
      etl_df = return_data_as_df(query,input_type= InputTypes.SQL, db_session= db_session)
      if len(etl_df) == 0:
         return_date = "2012-07-01"
      else:
         return_date = etl_df['elt_last_run_date'].iloc[0]
         does_etl_time_exists = True
   except Exception as e:
      suffix = str(e)
      error_prefix = ErrorHandling.RETURN_LAST_ETL_DATE_ERROR.value
   finally:
      return return_date, does_etl_time_exists
         






def excute_hook():
   sql_folder_path = "hook_SQL_commands"
   db_session = create_connection()

   etl_date , does_etl_time_exists = return_etl_last_updated_date(db_session)

   execute_sql_folder(db_session,sql_folder_path)

   close_connection()
