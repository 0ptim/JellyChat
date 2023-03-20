import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, make_response
from langchain import VectorDBQA, OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from data import init_db, add_rating, add_qa, get_qa

load_dotenv()

app = Flask(__name__)


with app.app_context():
    init_db()


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


@app.route("/ask", methods=["OPTIONS", "POST"])
def process_question():
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "API-Key, Content-Type",
            "Access-Control-Max-Age": "3600"
        }
        return make_response("", 204, headers)

    question: str = ""
    if request.is_json and 'question' in request.json:
        question = request.json["question"].strip()
        print("Question asked:", question)

    if question == "":
        return make_response("No question provided", 400)

    response = dbqa.run(question).strip()

    print(response)

    id = add_qa(question, response)

    resp = {"response": response, "id": id}
    headers = {"Access-Control-Allow-Origin": "*"}

    return make_response(jsonify(resp), 200, headers)


@app.route("/simulate", methods=["OPTIONS", "POST"])
def simulate_question():
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "API-Key, Content-Type",
            "Access-Control-Max-Age": "3600"
        }
        return make_response("", 204, headers)

    question: str = ""
    if request.is_json and 'question' in request.json:
        question = request.json["question"].strip()
        print("Question asked:", question)

    if question == "":
        return make_response("No question provided", 400)

    response = "You asked: " + question

    resp = {"response": response, "id": 0}
    headers = {"Access-Control-Allow-Origin": "*"}

    return make_response(jsonify(resp), 200, headers)


@app.route('/rate', methods=["OPTIONS", "POST"])
def add_QA():
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "API-Key, Content-Type",
            "Access-Control-Max-Age": "3600"
        }
        return make_response("", 204, headers)

    id = request.json['id']
    rating = request.json['rating']

    add_rating(id, rating)

    headers = {"Access-Control-Allow-Origin": "*"}

    return make_response("", 200, headers)


@app.route('/qa', methods=["OPTIONS", "GET"])
def get_QA():
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "API-Key, Content-Type",
            "Access-Control-Max-Age": "3600"
        }
        return make_response("", 204, headers)

    QA = get_qa()

    headers = {"Access-Control-Allow-Origin": "*"}

    return make_response(jsonify(QA), 200, headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("8080"), debug=False)
