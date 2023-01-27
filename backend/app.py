from flask import Flask
from flask import request

app = Flask(__name__)


@app.post("/get-response")
def process_question():
    if request.is_json and 'question' in request.json:
        question = request.json["question"]
        print("Question asked:", question)
    return {
        "respone": "Answer"
    }
