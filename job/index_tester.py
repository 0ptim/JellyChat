import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain import VectorDBQA, OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

collection_name = 'DeFiChainWiki'


client = QdrantClient(url=os.getenv('QDRANT_HOST'),
                      api_key=os.getenv('QDRANT_API_KEY'),
                      prefer_grpc=True)


embeddings = OpenAIEmbeddings()
qdrant = Qdrant(client=client,
                collection_name=collection_name,
                embedding_function=embeddings.embed_query)


dbqa = VectorDBQA.from_chain_type(
    llm=OpenAI(model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    vectorstore=qdrant,
    return_source_documents=False)


while True:
    question = input('Ask anything about DeFiChain: ')
    response = dbqa.run(question)
    print(response)
