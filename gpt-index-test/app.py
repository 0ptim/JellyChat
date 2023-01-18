from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader, GPTListIndex
import os

os.environ["OPENAI_API_KEY"] = ""

index_from_disk = GPTListIndex.load_from_disk('scraped_index.json')

response = index_from_disk.query(
    "How much DFI is needed to create a masternode?", verbose=True)
print(response)
