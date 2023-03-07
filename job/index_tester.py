from llama_index import GPTSimpleVectorIndex, LLMPredictor
from dotenv import load_dotenv
from langchain.llms import OpenAIChat
from llama_index.prompts.chat_prompts import CHAT_REFINE_PROMPT
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()

index_from_disk = GPTSimpleVectorIndex.load_from_disk(
    './indices/index_wiki.json')

llm_predictor = LLMPredictor(llm=OpenAIChat(
    temperature=0, model_name="gpt-3.5-turbo"))

while True:
    question = input('Ask anything about DeFiChain: ')
    response = index_from_disk.query(
        question,
        llm_predictor=llm_predictor,
        refine_template=CHAT_REFINE_PROMPT,
        similarity_top_k=1)
    print(response)
