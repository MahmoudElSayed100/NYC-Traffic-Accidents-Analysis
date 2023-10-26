from prehook import execute_prehook_csv
from hook import execute_hook
from posthook import execute_posthook

def etl_run():
   df,df2 = execute_prehook_csv()
   execute_hook(df,df2)
   execute_posthook()