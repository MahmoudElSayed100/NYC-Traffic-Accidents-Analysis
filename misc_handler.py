import requests
from database_handler import execute_query
import os
from lookups import ErrorHandling, ETLStep
from logging_handler import show_error_message
from datetime import datetime


def download_csv(csv_url, csv_folder):
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)
    # Generate today's date in yyyy-mm-dd format
    today_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{csv_folder}/all_accidents-{today_date}.csv"
    response = requests.get(csv_url)
    if response.status_code == 200:#(status success code)
        with open(file_name, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download CSV. Status code: {response.status_code}")   

def execute_sql_folder(db_session, sql_folder_path, etl_step):
    try:
        sql_files = [sqlfile for sqlfile in os.listdir(sql_folder_path) if sqlfile.endswith('.sql')]
        sorted_sql_files = sorted(sql_files)
        for sql_file in sorted_sql_files:
            file_etl_step = str(sql_file.split('-')[0].split('_')[1])
            if file_etl_step == etl_step.value:
                with open(os.path.join(sql_folder_path, sql_file), 'r') as file:
                    sql_query = file.read()
                    return_val = execute_query(db_session=db_session, query=sql_query)
                    if not return_val == ErrorHandling.NO_ERROR:
                        raise Exception(f"SQL File Error on SQL FILE = " + str(sql_file))
    except Exception as e:
        suffix = str(e)
        error_prefix = ErrorHandling.EXECUTE_SQL_FOLDER.value
        show_error_message(error_prefix, suffix)
        
