from gpt_index import GPTSimpleVectorIndex
from dotenv import load_dotenv

load_dotenv()

index_from_disk = GPTSimpleVectorIndex.load_from_disk('./indices/index_wiki.json')

while True:
    question = input('Ask anything about DeFiChain: ')
    response = index_from_disk.query(question, verbose=True, similarity_top_k=2)
    print(response)
