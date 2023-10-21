from prehook import execute_prehook_csv, execute_prehook_API
from hook import execute_hook
from posthook import execute_posthook
import time
import schedule

def etl_run():
   df = execute_prehook_csv()
   execute_hook(df)
   execute_posthook()

def etl_run_API():
   df = execute_prehook_API()
   execute_hook(df)
   execute_posthook()

# def etl_job():
#     print("Running ETL...")
#     start_time = time.time() 
#     etl_run()
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"ETL complete! Time elapsed: {elapsed_time:.2f} seconds")
   
# schedule.every(26).minutes.do(etl_job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)