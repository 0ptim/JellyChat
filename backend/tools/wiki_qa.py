from dotenv import load_dotenv, get_key
from supabase.client import Client, create_client
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import SupabaseVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.agents import Tool

load_dotenv()

# The name of the table in Supabase, where the vectors are stored
vectorTableName = "embeddings"

# Create the supabase client
supabase: Client = create_client(
    get_key(".env", "SUPABASE_URL"), get_key(".env", "SUPABASE_KEY")
)

# Create a vector store
embeddings = OpenAIEmbeddings()
vector_store = SupabaseVectorStore(
    embedding=embeddings,
    client=supabase,
    table_name=vectorTableName,
)

# Create a retriever
retriever = vector_store.as_retriever(search_type="similarity")


# Create retrieval chain
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
    chain_type="stuff",
    retriever=retriever,
)

description = """
Use this if you need to:
- Answer questions about the DeFiChain project.
- Lookup addresses of people.
Not useful, if you need to answer questions involving live-data.
Input should be a fully formed question."
"""

# Create a tool for agents to use
wikiTool = Tool(name="defichain_wiki_knowledge", description=description, func=qa.run)


if __name__ == "__main__":
    while True:
        question = input(
            "Ask something, that can be answered using information from DeFiChainWiki: "
        )
        result = qa({"query": question})
        print("✅ Answer:", result["result"])
