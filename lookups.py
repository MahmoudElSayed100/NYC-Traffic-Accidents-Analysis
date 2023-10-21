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
    EXECUTE_SQL_FOLDER = "Error in execute sql folder fucntion"
    DB_RETURN_INSERT_INTO_SQL_STMT_ERROR = "Error in return insert into sql statement function"
    EXECUTE_PREHOOK_ERROR = "Error in execute prehook function"
    ERROR_INSERT_STMNT = "Error in create insert statment fucntion"
    CL_HANDLER_REMOVE_SPACES_FROM_COLUMNS = "Error in remove spaces from columns function"
    CL_HANDLER_TRIM_SPACES_FROM_COLUMNS = " Error in trim spaces in datafram function"
    CL_HANDLER_REPLACE_NULL_WITH_OTHER = " Error in replace null values in borough with other function"
    CL_HANDLER_REPLACE_NULL_WITH_ON_STR_NAME = " Error in replace null values in borough with ON STREET NAME function"
    CL_HANDLER_REPLACE_NULL_WITH_OFF_STR_NAME = " Error in replace null values in borough with OFF STREET NAME function"
    CL_HANDLER_REPLACE_NULL_WITH_ZIP_CODE = "Error in replacing null in borough with zipcode function"
    CL_MAIN_FUNCTION = "Error in clean nyc traffic data function"
    RETURN_LAST_ETL_DATE_ERROR = "Error in return last etl updated date, hook "
    RETURN_INSERT_OR_UPDATE_LAST_ETL_ERROR = "Error in insert or update last etl checkpoint function"
    POSTHOOK_CLEANUP_ERROR = "Error in posthook cleanup function"
    EXECUTE_POSTHOOK_ERROR = "Error in execute posthook function"
    EXECUTE_HOOK_ERROR = "Error in execute hook function"
    HOOK_FILTER_DF_BY_ETL_DATE_ERROR = "Error in filter df by etl date "
    GET_NEWEST_CSV_FILE = "Error in get newest csv file function"
    RETURN_DATA_JSON_ERROR = "Error returning JSON"
    GET_DATA_FROM_API = "Error in get data from API Function"

class InputTypes(Enum):
    SQL = "SQL"
    CSV = "CSV"
    EXCEL = "Excel"
    JSON = "JSON"

class CSV_FOLDER_PATH(Enum):
    NAME = "csv_tables"

class DESTINATION_SCHEMA(Enum):
    DESTINATION_NAME = 'traffic_accidents'

class MAIN_SOURCE_URL(Enum):
   url = "https://data.cityofnewyork.us/api/views/yjf6-ewhz/rows.csv?accessType=DOWNLOAD"
   url2 = "https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD"