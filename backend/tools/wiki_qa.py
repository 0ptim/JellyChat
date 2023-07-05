import os
from dotenv import load_dotenv, get_key
from supabase.client import Client, create_client
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import SupabaseVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

load_dotenv()

# The name of the table in Supabase, where the vectors are stored
vectorTableName = "embeddings"

# Create the supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Create a vector store
embeddings = OpenAIEmbeddings()
vector_store = SupabaseVectorStore(
    embedding=embeddings,
    client=supabase,
    table_name=vectorTableName,
    query_name="match_embeddings",
)

# Create a retriever
retriever = vector_store.as_retriever(search_type="similarity")


# Create retrieval chain
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
    chain_type="stuff",
    retriever=retriever,
)


class ToolInputSchema(BaseModel):
    question: str = Field(..., description="A fully formed question.")


def get_answer(question: str) -> str:
    try:
        return qa(question)
    except Exception as e:
        return "The wiki knowledgebase is currently not available. We are working on it. Tell the user to use the wiki directly. https://www.defichainwiki.com/"


description = """Use this if you need to answer any question about DeFiChain which does not require live-data."""

wikiTool = StructuredTool(
    name="defichain_wiki_knowledge",
    description=description,
    func=get_answer,
    args_schema=ToolInputSchema,
)


if __name__ == "__main__":
    while True:
        question = input(
            "Ask something, that can be answered using information from DeFiChainWiki: "
        )
        result = qa({"query": question})
        print("✅ Answer:", result["result"])
