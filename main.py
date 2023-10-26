from prehook import execute_prehook
from hook import execute_hook
from posthook import execute_posthook

def etl_run():
   df,df2 = execute_prehook()
   execute_hook(df,df2)
   execute_posthook()