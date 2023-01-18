from gpt_index import GPTListIndex, SimpleWebPageReader, GPTSimpleVectorIndex
from IPython.display import Markdown, display
import os

os.environ["OPENAI_API_KEY"] = ""

documents = SimpleWebPageReader(html_to_text=True).load_data(
    ["https://www.defichainwiki.com/docs/auto/Staking"])

index = GPTListIndex(documents)
index.save_to_disk('scraped_index.json')
