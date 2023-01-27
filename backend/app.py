from gpt_index import GPTSimpleVectorIndex
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


load_dotenv()

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != os.environ["JWT_USERNAME"] or password != os.environ["JWT_PASSWORD"]:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


index_from_disk = GPTSimpleVectorIndex.load_from_disk(
    './indices/index_wiki.json')


@app.post("/get-response")
@jwt_required()
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
