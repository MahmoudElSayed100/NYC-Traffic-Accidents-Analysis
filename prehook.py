from database_handler import create_connection, close_connection, execute_query,return_create_statement_from_df_stg,return_data_as_df
from misc_handler import execute_sql_folder,download_csv
from lookups import ErrorHandling, InputTypes, ETLStep
from logging_handler import show_error_message
import os
from cleaning_dfs_handler import clean_nyc_traffic_data, clean_persons_table
import requests
import pandas as pd
import time

def get_newest_csv_file(csv_folder_path):
    try:
        files = os.listdir(csv_folder_path)
        csv_files = [file for file in files if file.endswith(".csv")]
        if not csv_files:
            print("No CSV files found in the download folder.")
            return None
        # Sort the CSV files by modification time (newest first)
        csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(csv_folder_path, x)), reverse=True)
        # Get the path of the newest CSV file
        newest_csv_file = os.path.join(csv_folder_path, csv_files[0])
        return newest_csv_file
    except Exception as e:
        suffix = str(e)
        error_prefix = ErrorHandling.GET_NEWEST_CSV_FILE.value
        show_error_message(error_prefix,suffix)

def get_and_read_source2_data_api():
    url = "https://data.cityofnewyork.us/resource/f55k-p6yu.json?$where=crash_date >= '2020-01-01T00:00:00'"
    response = requests.get(url, params={'$limit': 10000000})
    df = pd.DataFrame(response.json())
    return df



def execute_prehook():
    start_time = time.time()  # Record the start time
    df = None
    csv_folder = './csv_tables'
    url = "https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD"
    sql_folder_path = './SQL_commands'
    etl_step = ETLStep.PREHOOK
    try:
        table_name = "All_Accidents"
        table_name2 = "All_Injuries"
        db_session = create_connection()
        print("executing sql commands")
        execute_sql_folder(db_session, sql_folder_path, etl_step)
        print(f"Time taken for execute_sql_folder: {time.time() - start_time} seconds")

        start_time = time.time()  
        print("Extracting data from source 1")
        download_csv(url, csv_folder)
        print(f"Time taken for download_csv: {time.time() - start_time} seconds")

        start_time = time.time()
        print("Extracting data from source 2")
        df2 = get_and_read_source2_data_api()
        print(f"Time taken for get_and_read_source2_data_api: {time.time() - start_time} seconds")
        
        start_time = time.time()
        path = get_newest_csv_file(csv_folder)
        df = return_data_as_df(path, InputTypes.CSV, db_session)
        print(f"Time taken for return_data_as_df: {time.time() - start_time} seconds")

        start_time = time.time()
        print("Working on: cleaning df source 1")
        df = clean_nyc_traffic_data(df=df)
        print(f"Time taken for clean_nyc_traffic_data: {time.time() - start_time} seconds")

        start_time = time.time()
        print("Working on: cleaning dfs source 2")
        df2 = clean_persons_table(df2)
        print(f"Time taken for clean_persons_table: {time.time() - start_time} seconds")

        start_time = time.time()
        print("Creating create statement query for source 1")
        create_query = return_create_statement_from_df_stg(df, table_name)
        print(f"Time taken for return_create_statement_from_df_stg (source 1): {time.time() - start_time} seconds")

        start_time = time.time()
        print("Executing create statement query for source 1")
        execute_query(db_session, create_query)
        print(f"Time taken for execute_query (source 1): {time.time() - start_time} seconds")

        print("Created staging table for source 1")

        start_time = time.time()
        print("Creating create statement query for source 2")
        create_query2 = return_create_statement_from_df_stg(df2, table_name2)
        print(f"Time taken for return_create_statement_from_df_stg (source 2): {time.time() - start_time} seconds")

        start_time = time.time()
        print("Executing create statement query for source 2")
        execute_query(db_session, create_query2)
        print(f"Time taken for execute_query (source 2): {time.time() - start_time} seconds")

        print("Created staging table for source 2")

        close_connection(db_session)
        return df, df2
    except Exception as e:
        suffix = str(e)
        error_prefix = ErrorHandling.EXECUTE_PREHOOK_ERROR.value
        show_error_message(error_prefix, suffix)

    
