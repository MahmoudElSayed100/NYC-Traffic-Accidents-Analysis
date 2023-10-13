import pandas as pd
import requests


def download_and_read_csv(local_file_path, csv_url): 
   response = requests.get(csv_url)
   if response.status_code == 200: #(status success code)
      with open(local_file_path, 'wb') as file:
         file.write(response.content)
      df = pd.read_csv(local_file_path)
      return df
   else:
      print(f"Failed to download CSV. Status code: {response.status_code}")
      return None