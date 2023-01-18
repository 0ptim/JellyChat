from gpt_index import GPTListIndex, SimpleWebPageReader, GPTSimpleVectorIndex
from dotenv import load_dotenv

load_dotenv()

documents = SimpleWebPageReader(html_to_text=True).load_data(
    ["https://www.defichainwiki.com/docs/auto/Staking"])

index = GPTListIndex(documents)
index.save_to_disk('scraped_index.json')
