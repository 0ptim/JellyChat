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
                embedding_function=embeddings.embed_query)

# Create a qdrant retriever
retriever = qdrant.as_retriever(search_type="similarity")


# Create retrieval chain
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=retriever)

# Create a tool for agents to use
wikiTool = Tool(
    name="DeFiChainWiki QA System",
    description="For information all around the DeFiChain project with it's ecosystem of projects and products. Not useful, if you need to answer questions involving live-data. Input should be a fully formed question.",
    func=qa.run
)


# Debugging
# Add this to `RetrievalQA.from_chain_type`: source_documents=True
# while True:
#     question = input('Ask anything about DeFiChain: ')
#     result = qa({"query": question})
#     # Print the documents
#     for document in result["source_documents"]:
#         print("📑 Document", document)
#     # Print the answer
#     print("✅ Answer:", result["result"])
