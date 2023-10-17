from database_handler import create_connection, close_connection, execute_query,return_create_statement_from_df_stg,return_insert_into_sql_statement_from_df_stg
from misc_handler import download_and_read_csv, execute_sql_folder
from lookups import ErrorHandling, CSV_FOLDER_PATH
from logging_handler import show_error_message
import os
from cleaning_dfs_handler import clean_nyc_traffic_data


#download, read, clean and create stg tables
def get_cleaned_data_from_csv_into_staging(db_session):
    table_name = "All_Accidents"
    path=r"C:\Users\Admin\Desktop\SEF-Final-Project-NYC-Accidents-Analysis\csv_tables\test.csv"
    # url = "https://data.cityofnewyork.us/api/views/yjf6-ewhz/rows.csv?accessType=DOWNLOAD"
    url= "https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD"
    print("Working on: Download and read")
    df = download_and_read_csv(path, url)
    print("Done: Download and read")
    print("Working on: cleaning df")
    df = clean_nyc_traffic_data(df)
    print("Done: Cleaning df")
    print("Createing create statement query")
    create_query = return_create_statement_from_df_stg(df,table_name,)
    print("Executing create statment query")
    execute_query(db_session,create_query)
    print("Created staging tables")
    print("Creating insert into staging tables from df")
    insert_query = return_insert_into_sql_statement_from_df_stg(df,table_name)
    print("inserting data into stg")
    for query in insert_query:
        execute_query(db_session,query)
    print("Success")





def execute_prehook(sql_folder_path ="SQL_commands"):
   try:
      db_session = create_connection()

      execute_sql_folder(db_session , sql_folder_path)

      get_cleaned_data_from_csv_into_staging(db_session)

      close_connection(db_session)
   except Exception as e:
       suffix = str(e)
       error_prefix = ErrorHandling.EXECUTE_PREHOOK_ERROR.value
       show_error_message(error_prefix,suffix)