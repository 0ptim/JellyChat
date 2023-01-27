from gpt_index import GPTSimpleVectorIndex
from dotenv import load_dotenv
from flask import Flask
from flask import request

load_dotenv()

index_from_disk = GPTSimpleVectorIndex.load_from_disk(
    './indices/index_wiki.json')

app = Flask(__name__)


@app.post("/get-response")
def process_question():
    print("▶️")

    if request.is_json and 'question' in request.json:
        question = request.json["question"]
        print("Question asked:", question)

    response = index_from_disk.query(
        question, verbose=True, similarity_top_k=1)
    print(response)

    return {
        "response": response.response
    }
