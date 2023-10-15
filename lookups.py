from enum import Enum

class ErrorHandling(Enum):
    DB_CONNECT_ERROR = "DB Connection Error"
    DB_RETURN_QUERY_ERROR = "DB Return Query Error"
    API_ERROR = "Error calling API"
    RETURN_DATA_CSV_ERROR = "Error returning CSV"
    RETURN_DATA_EXCEL_ERROR = "Error returning Excel"
    RETURN_DATA_SQL_ERROR = "Error returning SQL"
    RETURN_DATA_UNDEFINED_ERROR = "Cannot find File type"
    EXECUTE_QUERY_ERROR = "Error executing the query"
    NO_ERROR = "No Errors"
    DB_RETURN_INSERT_INTO_SQL_STMT_STG_ERROR = "Error in insert into sql statement (stg)"
    DB_RETURN_CREATE_STMT_FROM_DF_STG_ERROR = "Error in create statement from df (stg)"
    CLOSE_CONNECTION_ERROR = "Error in closing connection"
    PREHOOK_EXECUTE_SQL_FOLDER = "Error in prehook, execute sql folder fucntion"
    DB_RETURN_INSERT_INTO_SQL_STMT_ERROR = "Error in return insert into sql statement function"
    EXECUTE_PREHOOK_ERROR = "Error in execute prehook function"
    ERROR_INSERT_STMNT = "Error in create insert statment fucntion"
    CL_HANDLER_REMOVE_SPACES_FROM_COLUMNS = "Error in remove spaces from columns function"
    CL_HANDLER_TRIM_SPACES_FROM_COLUMNS = " Error in trim spaces in datafram function"
    CL_HANDLER_REPLACE_NULL_WITH_OTHER = " Error in replace null values in borough with other function"
    CL_HANDLER_REPLACE_NULL_WITH_ON_STR_NAME = " Error in replace null values in borough with ON STREET NAME function"
    CL_HANDLER_REPLACE_NULL_WITH_OFF_STR_NAME = " Error in replace null values in borough with OFF STREET NAME function"
    CL_MAIN_FUNCTION = "Error in clean nyc traffic data function"

class InputTypes(Enum):
    SQL = "SQL"
    CSV = "CSV"
    EXCEL = "Excel"

class CSV_FOLDER_PATH(Enum):
    NAME = "csv_tables"

class DESTINATION_SCHEMA(Enum):
    DESTINATION_NAME = 'traffic_accidents'

class MAIN_SOURCE_URL(Enum):
   url = "https://data.cityofnewyork.us/api/views/yjf6-ewhz/rows.csv?accessType=DOWNLOAD"
   
class FIRST_CSV_FILE_PATH(Enum):
   local_file_path = r"C:\Users\Admin\Desktop\SEF-Final-Project-NYC-Accidents-Analysis\csv_tables\test.csv"