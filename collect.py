# %%
import pandas as pd
import requests
import dotenv
import os
import argparse
import json
dotenv.load_dotenv()

TOKEN = os.getenv("REVERB_TOKEN")

# %%
class Collector:

    def __init__(self, token:str, output_folder:str="data/raw"):
        self.token = token
        self.output_folder = output_folder

    def get_headers(self)-> dict:

        headers = {
        "Authorization": f"Bearer {self.token}",
        "Accept": "application/hal+json",
        "Accept-version": "3.0"
        }
        return headers

    def to_dict(self, df):

        for col in df.columns:
            if df[col].apply(
                    lambda x: isinstance(x, (dict,list))).any():
                    df[col] = df[col].apply(lambda x: json.dumps(x)
                    if isinstance(x, (dict, list)) else None)
        return df

    def save_data(self, listings:list, batch_number:int)-> None:

        if not listings:
            return
        
        os.makedirs(self.output_folder,
                    exist_ok=True) 

        path = f"{self.output_folder}/listings_{batch_number:02}.parquet"

        df = pd.DataFrame(listings)
        self.to_dict(df)
        df.to_parquet(path, index=False)

    def extract_data(self, n_batches:int, pages_per_batch:int=100, 
                    start_page:int=1, batch_number:int=0)-> None:

        headers = self.get_headers()

        finished = False

        for _ in range(n_batches):
        
            all_listings = []

            for page in range(start_page, start_page + pages_per_batch):

                try:
                    url = f"https://api.reverb.com/api/listings?page={page}"
                    resp = requests.get(url=url, headers=headers, timeout=30)
                    resp.raise_for_status()
                    data = resp.json()
                

                except requests.exceptions.RequestException as err:
                    print(err)
                    finished = True
                    break            

                all_listings.extend(data["listings"])
                
                print(f"Page {page}")

                

            self.save_data(all_listings, batch_number)
            batch_number += 1
            start_page = page + 1
            
            if finished:
                break


# %%

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--n_batches', type=int, default=10, help="Número de batches para processar")
    parser.add_argument('--pages_per_batch', type=int, default=100, help="Quantidade de páginas em cada batch")
    parser.add_argument('--start_page', type=int, default=1, help="Página inicial da extração")
    parser.add_argument('--start_batch', type=int, default=0, help="Número inicial do batch/parquet")

    args = parser.parse_args()

    collect = Collector(TOKEN)
    collect.extract_data(args.n_batches, args.pages_per_batch, args.start_page, args.start_batch)
