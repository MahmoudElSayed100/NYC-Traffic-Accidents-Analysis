from prehook import execute_prehook_csv, execute_prehook_API
from hook import execute_hook, execute_hook_API
from posthook import execute_posthook
import time
import schedule

def etl_run():
   df,df2 = execute_prehook_csv()
   execute_hook(df,df2)
   execute_posthook()