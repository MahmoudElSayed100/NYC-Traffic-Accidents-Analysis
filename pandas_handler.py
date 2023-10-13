import os
from lookups import ErrorHandling,CSV_FOLDER_PATH
from logging_handler import show_error_message
import pandas as pd


def get_csv_file_names_into_dict(folder_path=CSV_FOLDER_PATH.NAME.value):
    try:
        csv_files_dict = {}
        for filename in os.listdir(folder_path):
            if filename[-4:] == ".csv":
                csv_files_dict[filename] = None
    except Exception as e:
        error_string_prefix = ErrorHandling.CSV_ERROR.value
        error_string_suffix = str(e)
        show_error_message(error_string_prefix, error_string_suffix)
    finally:
        return csv_files_dict