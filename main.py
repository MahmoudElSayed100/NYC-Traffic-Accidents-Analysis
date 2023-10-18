from prehook import execute_prehook
from hook import excute_hook
from posthook import execute_posthook

def etl_run():
   execute_prehook()
   excute_hook()
   execute_posthook()