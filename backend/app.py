from gpt_index import GPTSimpleVectorIndex
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request
from flask import request


load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

index_from_disk = GPTSimpleVectorIndex.load_from_disk(
    './indices/index_wiki.json')


@app.post("/ask")
def process_question():
    if request.headers.get("API-Key") != API_KEY:
        return "Unauthorized", 401

    if request.is_json and 'question' in request.json:
        question = request.json["question"]
        print("Question asked:", question)

    response = index_from_disk.query(
        question, verbose=True, similarity_top_k=1)
    print(response)

    return {
        "response": response.response
    }


@app.post("/simulate")
def simulate_question():
    if request.headers.get("API-Key") != API_KEY:
        return "Unauthorized", 401

    if request.is_json and 'question' in request.json:
        question = request.json["question"]
        print("Question asked:", question)

    response = "You asked: " + question
    print(response)

    return {
        "response": response
    }
