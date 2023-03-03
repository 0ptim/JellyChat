from llama_index import GPTSimpleVectorIndex
from dotenv import load_dotenv
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()

index_from_disk = GPTSimpleVectorIndex.load_from_disk(
    './indices/index_wiki.json')

while True:
    question = input('Ask anything about DeFiChain: ')
    response = index_from_disk.query(
        question, similarity_top_k=1)
    print(response)
