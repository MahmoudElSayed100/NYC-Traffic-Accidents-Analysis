import psycopg2
import pandas as pd
from lookups import ErrorHandling, InputTypes, DESTINATION_SCHEMA
from logging_handler import show_error_message

config_dict = {
    "host"      : "localhost",
    "database"  : "NYCTrafficAccidents",
    "user"      : "postgres",
    "password"  : "M@rkseven11"
}
def create_connection():
    db_session = None
    try:
        db_session = psycopg2.connect(**config_dict)
    except Exception as e:
        error_prefix = ErrorHandling.DB_CONNECT_ERROR.value
        suffix = str(e)
        show_error_message(error_prefix, suffix)
    finally:
        return db_session

def return_query(db_session,query):
    results = None
    try:
        cursor = db_session.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        db_session.commit()
    except Exception as e:
        error_prefix = ErrorHandling.DB_RETURN_QUERY_ERROR.value
        suffix = str(e)
        show_error_message(error_prefix, suffix)
    finally:
        return results
    
def return_data_as_df(file_executor, input_type, db_session = None):
    return_dataframe = None
    try:
        if input_type == InputTypes.CSV:
            return_dataframe = pd.read_csv(file_executor)
        elif input_type == InputTypes.SQL:
            return_dataframe = pd.read_sql_query(con= db_session, sql= file_executor)
        else:
            raise Exception("The file type does not exist, please check main function")
    except Exception as e:
        if input_type == InputTypes.CSV:
            suffix = str(e)
            error_prefix = ErrorHandling.RETURN_DATA_CSV_ERROR.value
        elif input_type == InputTypes.SQL:
            suffix = str(e)
            error_prefix = ErrorHandling.RETURN_DATA_SQL_ERROR.value
        else:
            error_prefix = ErrorHandling.RETURN_DATA_UNDEFINED_ERROR.value
            show_error_message(error_prefix, suffix)
    finally:
         return return_dataframe

def execute_query(db_session, query):
    return_val = ErrorHandling.NO_ERROR
    try:
        cursor = db_session.cursor()
        cursor.execute(query)
        db_session.commit()
    except Exception as e:
        error_prefix = ErrorHandling.EXECUTE_QUERY_ERROR.value
        return_val = error_prefix
        suffix = str(e)
        show_error_message(error_prefix, suffix)
    finally:
        return return_val

def return_create_statement_from_df_stg(dataframe, table_name, schema_name=DESTINATION_SCHEMA.DESTINATION_NAME.value):
    type_mapping = {
        'int64':'INT',
        'float64':'FLOAT',
        'datetime64[ns]': 'TIMESTAMP',
        'bool':'BOOLEAN',
        'object': 'TEXT'
    }
    try:
      fields = []
      for column, dtype in dataframe.dtypes.items():
         sql_type = type_mapping.get(str(dtype), 'TEXT')
         fields.append(f"{column} {sql_type}")
      
      create_table_statemnt = f"CREATE TABLE IF NOT EXISTS {schema_name}.stg_{table_name} (\n "
      create_table_statemnt += ", \n ".join(fields)
      create_table_statemnt += " \n );"
      create_index_statement = ""
      return create_table_statemnt
    except Exception as e:
        error_prefix = ErrorHandling.DB_RETURN_CREATE_STMT_FROM_DF_STG_ERROR.value
        suffix = str(e)
        show_error_message(error_prefix, suffix)

def return_insert_into_sql_statement_from_df_stg(dataframe, table_name, schema_name=DESTINATION_SCHEMA.DESTINATION_NAME.value):
    try:
        columns = ', '.join(dataframe.columns)
        insert_statement_list = []
        for _, row in dataframe.iterrows():
            value_strs = []
            for val in row.values:
                if pd.isna(val):
                    value_strs.append("NULL")
                elif isinstance(val, (str)):
                    val_escaped = val.replace("'", "''")
                    value_strs.append(f"'{val_escaped}'")
                else:
                    value_strs.append(f"'{val}'")
            values = ', '.join(value_strs)
            insert_statement = f'INSERT INTO {schema_name}.stg_{table_name} ({columns}) VALUES ({values});'
            insert_statement_list.append(insert_statement)
        return insert_statement_list
    except Exception as e:
        error_prefix = ErrorHandling.DB_RETURN_INSERT_INTO_SQL_STMT_STG_ERROR.value
        suffix = str(e)
        show_error_message(error_prefix, suffix)
                  

def close_connection(db_session):
    try:
        db_session.close()
    except Exception as e:
        suffix = str(e)
        error_prefix = ErrorHandling.CLOSE_CONNECTION_ERROR.value
        show_error_message(error_prefix,suffix)