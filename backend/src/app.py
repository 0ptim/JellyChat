from gpt_index import GPTSimpleVectorIndex
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request, make_response
from flask import request


load_dotenv()

app = Flask(__name__)

index_from_disk = GPTSimpleVectorIndex.load_from_disk(
    './indices/index_wiki.json')


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
        question = request.json["question"]
        print("Question asked:", question)

    response = index_from_disk.query(
        question, verbose=True, similarity_top_k=1)
    print(response)

    resp = {"response": response}
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
        question = request.json["question"]
        print("Question asked:", question)

    response = "You asked: " + question

    resp = {"response": response}
    headers = {"Access-Control-Allow-Origin": "*"}

    return make_response(jsonify(resp), 200, headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("8080"), debug=False)
