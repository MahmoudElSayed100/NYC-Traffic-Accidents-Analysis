from database_handler import create_connection, close_connection, execute_query,return_create_statement_from_df_stg,return_insert_into_sql_statement_from_df_stg
from misc_handler import download_and_read_csv
from lookups import ErrorHandling, CSV_FOLDER_PATH
from logging_handler import show_error_message
import os
from cleaning_dfs_handler import clean_nyc_traffic_data


def execute_sql_folder(db_session, sql_folder_path):
    try:
        sql_files = [sqlfile for sqlfile in os.listdir(sql_folder_path) if sqlfile.endswith('.sql')]
        sorted_sql_files =  sorted(sql_files)
        for sql_file in sorted_sql_files:
            with open(os.path.join(sql_folder_path,sql_file), 'r') as file:
                sql_query = file.read()
                return_val = execute_query(db_session= db_session, query= sql_query)
                if not return_val == ErrorHandling.NO_ERROR:
                    raise Exception(f"  SQL File Error on SQL FILE = " +  str(sql_file))
    except Exception as e:
        suffix = str(e)
        error_prefix = ErrorHandling.PREHOOK_EXECUTE_SQL_FOLDER.value
        show_error_message(error_prefix, suffix)
#download, read, clean and create stg tables
def CSV_Full(db_session):
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





def execute_prehook(sql_folder_path =r"C:\Users\Admin\Desktop\SEF-Final-Project-NYC-Accidents-Analysis\SQL_commands"):
   try:
      db_session = create_connection()

      execute_sql_folder(db_session , sql_folder_path)

      CSV_Full(db_session)

      close_connection(db_session)
   except Exception as e:
       suffix = str(e)
       error_prefix = ErrorHandling.EXECUTE_PREHOOK_ERROR.value
       show_error_message(error_prefix,suffix)