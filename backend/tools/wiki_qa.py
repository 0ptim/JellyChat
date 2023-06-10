import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.agents import Tool

load_dotenv()

# The name of the collection in Qdrant
collection_name = 'DeFiChainWiki'


# Create a Qdrant client
client = QdrantClient(url=os.getenv('QDRANT_HOST'),
                      api_key=os.getenv('QDRANT_API_KEY'),
                      prefer_grpc=True)


# Create a langchain qdrant object
embeddings = OpenAIEmbeddings()
qdrant = Qdrant(client=client,
                collection_name=collection_name,
                embeddings=embeddings)

# Create a qdrant retriever
retriever = qdrant.as_retriever(search_type="similarity")


# Create retrieval chain
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
    chain_type="stuff",
    retriever=retriever
)

description = """
Use this if you need to:
- Answer questions about the DeFiChain project.
- Lookup addresses of people.
Not useful, if you need to answer questions involving live-data.
Input should be a fully formed question."
"""

# Create a tool for agents to use
wikiTool = Tool(
    name="DeFiChainWiki knowledge base",
    description=description,
    func=qa.run
)


if __name__ == '__main__':
    while True:
        question = input(
            'Ask something, that can be answered using information from DeFiChainWiki: ')
        result = qa({"query": question})
        print("✅ Answer:", result["result"])
