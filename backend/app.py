from gpt_index import GPTSimpleVectorIndex
from dotenv import load_dotenv
from flask import Flask, jsonify, request, make_response
from flask import request
import logging
import sys
from data import get_db, init_db, add_rating

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()

app = Flask(__name__)


with app.app_context():
    init_db()


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

    if question == "":
        return make_response("No question provided", 400)

    response = index_from_disk.query(
        question, similarity_top_k=1)
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

    if question == "":
        return make_response("No question provided", 400)

    response = "You asked: " + question

    resp = {"response": response}
    headers = {"Access-Control-Allow-Origin": "*"}

    return make_response(jsonify(resp), 200, headers)


@app.route('/rate', methods=['POST'])
def add_qa():
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "API-Key, Content-Type",
            "Access-Control-Max-Age": "3600"
        }
        return make_response("", 204, headers)

    question = request.json['question']
    answer = request.json['answer']
    rating = request.json['rating']

    add_rating(question, answer, rating)

    return 'Rating added'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("8080"), debug=False)
