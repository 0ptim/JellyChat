import os
import json
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from supabase.client import Client, create_client
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.tools import StructuredTool
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
import langchain


load_dotenv()

# Set debug to True to see A LOT of details of langchain's inner workings
langchain.debug = True

# The name of the table in Supabase, where the vectors are stored
vectorTableName = "embeddings"

# Create the supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class ToolInputSchema(BaseModel):
    question: str = Field(..., description="A fully formed question.")


class KnowledgeAnswer(BaseModel):
    answer: str = Field(..., description="The answer to the question.")
    sources: List[str] = Field(
        ...,
        description="The sources which contributed to the answer.",
    )


llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.7)

prompt_msgs = [
    SystemMessagePromptTemplate.from_template(
        """You're an elite algorithm, answering queries based solely on given context. If the context lacks the answer, state ignorance.
        
        Context:
        {context}"""
    ),
    HumanMessagePromptTemplate.from_template("{question}"),
]
prompt = ChatPromptTemplate.from_messages(prompt_msgs)

chain = create_structured_output_chain(KnowledgeAnswer, llm, prompt)


def get_answer(question: str) -> str:
    try:
        vectors = OpenAIEmbeddings().embed_documents([question])
        embeddings = supabase.rpc(
            "match_embeddings", dict(query_embedding=vectors[0], match_count=7)
        ).execute()

        print(f"⚡ Retrieved {len(embeddings.data)} vectors from Supabase:")
        for entry in embeddings.data:
            print("🔖 Title:", entry["metadata"]["title"])
            print("🌐 Source:", entry["metadata"]["source"])
            print("📊 Similarity:", entry["similarity"])
            print("📄 Content:", entry["content"].replace("\n", " ")[:100] + "...")
            print("-" * 50)

        result = chain.run(context=json.dumps(embeddings.data), question=question)
        print("📝", result)

        return f"""Answer: {result.answer}
        Sources: {json.dumps(result.sources)}
        """

    except Exception as e:
        print(e)
        return "The wiki knowledgebase is currently not available. We are working on it. Tell the user to use the wiki directly. https://www.defichainwiki.com/"


description = """Use this if you need to answer any question about DeFiChain which does not require live-data. Make sure to include the source of the answer in your response."""

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
        print("✅", get_answer(question))
