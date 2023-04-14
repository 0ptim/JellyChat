import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

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
    llm=OpenAI(model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False)


while True:
    question = input('Ask anything about DeFiChain: ')
    response = qa.run(question)
    print(response)
