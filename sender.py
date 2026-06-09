# %%

import boto3
import dotenv
import os
import argparse

dotenv.load_dotenv()

s3 = boto3.resource('s3')

AWS_KEY = os.getenv("AWS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

# %%

class Sender:
    def __init__(self, bucket_name:str, bucket_folder:str)->None:
        
        self.bucket_name = bucket_name
        self.bucket_folder = bucket_folder

        self.s3 = boto3.client("s3",
                               aws_access_key_id = AWS_KEY,
                               aws_secret_access_key = AWS_SECRET_KEY,
                               region_name = 'us-east-2')
        
    def process_file(self, filename:str)->bool:

        file = os.path.basename(filename)
        bucket_path = f"{self.bucket_folder}/{file}"

        try:
            self.s3.upload_file(filename, self.bucket_name, bucket_path)
        
        except Exception as err:
            print(err)
            return False
        
        os.remove(filename)
        return True
    
    def process_folder(self, folder:str)->None:

        files = os.listdir(folder)

        for f in files:
            self.process_file(os.path.join(folder, f))

# %%
if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--bucket_name", type=str, default="datalake-raw-ssm")
    parser.add_argument("--bucket_folder", type=str, default="reverb/results")
    parser.add_argument("--folder", type=str, default="data/raw")

    args = parser.parse_args()

    send = Sender(args.bucket_name, args.bucket_folder)
    send.process_folder(args.folder)
# %%
