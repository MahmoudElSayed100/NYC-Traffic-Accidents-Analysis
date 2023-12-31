import logging
from database_handler import create_connection, close_connection, execute_query
from lookups import ErrorHandling, DESTINATION_SCHEMA
from logging_handler import show_error_message
import time

def posthook_cleanup(db_session):
   destination_table = DESTINATION_SCHEMA.DESTINATION_NAME.value
   query = f"""
   TRUNCATE TABLE {destination_table}.stg_all_accidents RESTART IDENTITY CASCADE;
   TRUNCATE TABLE {destination_table}.stg_all_injuries RESTART IDENTITY CASCADE;
   """
   try:
      execute_query(db_session=db_session, query=query)
   except Exception as e:
      suffix = str(e)
      error_prefix = ErrorHandling.POSTHOOK_CLEANUP_ERROR.value
      show_error_message(error_prefix, suffix)

def execute_posthook():
   start_time = time.time()
   try:
      db_session = create_connection()
      print("executing post hook")
      posthook_cleanup(db_session=db_session)
      print("stg table 1 truncated!")
      print("stg table 2 truncated!")
      close_connection(db_session=db_session)
      print("Success")
      logging.info(f"Time taken for execute_posthook : { time.time() - start_time}")
   except Exception as e:
      suffix = str(e)
      error_prefix = ErrorHandling.EXECUTE_POSTHOOK_ERROR.value
      show_error_message(error_prefix, suffix)