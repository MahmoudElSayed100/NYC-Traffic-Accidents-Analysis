from database_handler import create_connection, close_connection, execute_query,return_create_statement_from_df_stg,return_data_as_df
from misc_handler import execute_sql_folder,get_data_via_api,download_csv
from lookups import ErrorHandling, InputTypes
from logging_handler import show_error_message
import os
from cleaning_dfs_handler import clean_nyc_traffic_data, clean_persons_table
from cleaning_dfs_handler_API import clean_nyc_traffic_data_API
import requests
import pandas as pd

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


def execute_prehook_csv():
    df = None
    csv_folder = r'C:\Users\Admin\Desktop\NYC-TRAFFIC-ACCIDENTS-PROJECT\csv_tables'
    url = "https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD"
    sql_folder_path = 'SQL_commands'
    try:
        table_name = "All_Accidents"
        table_name2 = "All_Injuries"
        db_session = create_connection()
        print("executing sql commands")
        execute_sql_folder(db_session , sql_folder_path)
        print("Extracting data from source 1")
        download_csv(url,csv_folder)
        print("done")
        print("Extracting data from source 2")
        df2 = get_and_read_source2_data_api()
        path = get_newest_csv_file(csv_folder)
        df = return_data_as_df(path,InputTypes.CSV,db_session)
        print("Working on: cleaning df source 1")
        df = clean_nyc_traffic_data(df = df)
        print("done")
        print("Working on: cleaning dfs source 2")
        df2 = clean_persons_table(df2)
        print("done")
        print("Createing create statement query for source 1")
        create_query = return_create_statement_from_df_stg(df,table_name)
        print("Executing create statment query")
        execute_query(db_session,create_query)
        print("Created staging table for source 1")
        print("Creating create statement query for source 2")
        create_query2 = return_create_statement_from_df_stg(df2,table_name2)
        print("Executing create statement query")
        execute_query(db_session,create_query2)
        print("Created staging table for source 2")
        close_connection(db_session)
        return df, df2
    except Exception as e:
        suffix = str(e)
        error_prefix = ErrorHandling.EXECUTE_PREHOOK_ERROR.value
        show_error_message(error_prefix,suffix)
    
def execute_prehook_API():
    df = None
    csv_folder = r"C:\Users\Admin\Desktop\SEF-Final-Project-NYC-Accidents-Analysis\csv_tables"
    url = "https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD"
    sql_folder_path =r"C:\Users\Admin\Desktop\SEF-Final-Project-NYC-Accidents-Analysis\SQL_commands"
    try:
        table_name = "All_Accidents"
        db_session = create_connection()
        print("executing sql commands")
        execute_sql_folder(db_session , sql_folder_path)
        print("Extracting data")
        df = get_data_via_api()
        print("done")
        print("Working on: cleaning df")
        df = clean_nyc_traffic_data_API(df)
        print("done")
        print("Createing create statement query")
        create_query = return_create_statement_from_df_stg(df,table_name)
        print("Executing create statment query")
        execute_query(db_session,create_query)
        print("Created staging tables")
        close_connection(db_session)
    except Exception as e:
        suffix = str(e)
        error_prefix = ErrorHandling.EXECUTE_PREHOOK_ERROR.value
        show_error_message(error_prefix,suffix)
    finally:
        return df