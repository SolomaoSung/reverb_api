# %%
import os
from collect import Collector
from sender import Sender
import dotenv

dotenv.load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
TOKEN = os.getenv("REVERB_TOKEN")

# %%

def processo():

    print("Iniciando processo...")

    print("Coletando dados...")
    collect = Collector(TOKEN, output_folder="data/raw")
    collect.extract_data(10)

    print("Enviando dados...")
    sender = Sender(bucket_name=BUCKET_NAME, bucket_folder="reverb/results")
    sender.process_folder("data/raw")

processo()
# %%
