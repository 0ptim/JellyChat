import openai
import pandas as pd
import numpy as np
import pickle
from transformers import GPT2TokenizerFast
from typing import List

openai.api_key = ""
COMPLETIONS_MODEL = "text-davinci-003"

## Step 0: Prevent hallucination with prompt engineering
# prompt = """Answer the question as truthfully as possible using the provided text, and if the answer is not contained within the text below, say "I don't know"
#
# Context:
# DeFiChain uses a Proof-of-Stake (PoS) model in order to secure the network. Users must stake an amount of DFI to create a masternode. Masternodes are nodes that are allowed to create blocks, in return for block rewards. In case of malicious intent by a masternode, it is banned. This way, malicious actors cannot gain control of the network unless they have a large amount of DFI to stake. It is important to note, banned masternodes do not happen accidentally, they are only caused by malicious users.
# Currently, the amount of DFI that is required to stake is 20,000 DFI, although it is possible to use a service provider such as Cake to stake less than that amount.
#
# Q: What consensus mechanism does DeFiChain use?
# A:"""

# a = openai.Completion.create(
#     prompt=prompt,
#     temperature=0,
#     max_tokens=300,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0,
#     model=COMPLETIONS_MODEL
# )["choices"][0]["text"].strip(" \n")
#
# print(a)


MODEL_NAME = "curie"

DOC_EMBEDDINGS_MODEL = f"text-search-{MODEL_NAME}-doc-001"
QUERY_EMBEDDINGS_MODEL = f"text-search-{MODEL_NAME}-query-001"


def get_embedding(text: str, model: str) -> List[float]:
    result = openai.Embedding.create(
        model=model,
        input=text)
    return result["data"][0]["embedding"]


def get_doc_embedding(text: str) -> List[float]:
    return get_embedding(text, DOC_EMBEDDINGS_MODEL)


def get_query_embedding(text: str) -> List[float]:
    return get_embedding(text, QUERY_EMBEDDINGS_MODEL)


def compute_doc_embeddings(df: pd.DataFrame) -> dict[tuple[str, str], List[float]]:
    """
    Create an embedding for each row in the dataframe using the OpenAI Embeddings API.

    Return a dictionary that maps between each embedding vector and the index of the row that it corresponds to.
    """
    return {
        idx: get_doc_embedding(r.content.replace("\n", " ")) for idx, r in df.iterrows()
    }


def load_embeddings(fname: str) -> dict[tuple[str, str], List[float]]:
    """
    Read the document embeddings and their keys from a CSV.

    fname is the path to a CSV with exactly these named columns:
        "title", "heading", "0", "1", ... up to the length of the embedding vectors.
    """

    df = pd.read_csv(fname, header=0)
    max_dim = max([int(c) for c in df.columns if c != "title" and c != "heading"])
    return {
        (r.title, r.heading): [r[str(i)] for i in range(max_dim + 1)] for _, r in df.iterrows()
    }


document_embeddings = load_embeddings("https://cdn.openai.com/API/examples/data/olympics_sections_document_embeddings.csv")


# An example embedding:
example_entry = list(document_embeddings.items())[0]
print(f"{example_entry[0]} : {example_entry[1][:5]}... ({len(example_entry[1])} entries)")

def vector_similarity(x: List[float], y: List[float]) -> float:
    """
    We could use cosine similarity or dot product to calculate the similarity between vectors.
    In practice, we have found it makes little difference.
    """
    return np.dot(np.array(x), np.array(y))


def order_document_sections_by_query_similarity(query: str, contexts: dict[tuple[str, str], np.array]) -> List[
    tuple[float, tuple[str, str]]]:
    """
    Find the query embedding for the supplied query, and compare it against all the pre-calculated document embeddings
    to find the most relevant sections.

    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = get_query_embedding(query)

    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)

    return document_similarities


print(order_document_sections_by_query_similarity("Who won the men's high jump?", document_embeddings)[:5])
