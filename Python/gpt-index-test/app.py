from gpt_index import GPTListIndex
from dotenv import load_dotenv

load_dotenv()

index_from_disk = GPTListIndex.load_from_disk('scraped_index.json')

response = index_from_disk.query(
    "How much DFI is needed to create a masternode?", verbose=True)
print(response)
