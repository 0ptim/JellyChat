# Imports
from dotenv import load_dotenv
from flask import Flask, jsonify, request, make_response
from langchain.callbacks import get_openai_callback
from chat_agent import agent_for_user
from data import init_db, add_rating, add_qa, get_qa

# Setup
load_dotenv()
app = Flask(__name__)

with app.app_context():
    init_db()

# CORS headers
headers_cors = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST",
    "Access-Control-Allow-Headers": "API-Key, Content-Type",
    "Access-Control-Max-Age": "3600",
}


# Helper function to extract data from JSON request
def extract_data(json_request, field):
    return json_request.get(field, "").strip()


@app.route("/ask", methods=["OPTIONS", "POST"])
def process_question():
    if request.method == "OPTIONS":
        return make_response("", 204, headers_cors)

    if not request.is_json:
        return make_response("Request should be in JSON format", 400)

    user_token = extract_data(request.json, "user_token")
    if not user_token:
        return jsonify({"error": "User token is required"}), 400

    question = extract_data(request.json, "question")
    if not question:
        return jsonify({"error": "Question is required"}), 400

    jelly_chat_agent = agent_for_user(user_token)

    with get_openai_callback() as cb:
        response_obj = jelly_chat_agent(question)
        log_response_info(response_obj, cb)

    response = response_obj["output"].strip()
    qa_id = add_qa(question, response)

    return make_response(jsonify({"response": response, "id": qa_id}), 200, headers_cors)


def log_response_info(response_obj, callback_obj):
    print(f"🔥 Response object: {response_obj}")
    print(f"Total Tokens: {callback_obj.total_tokens}")
    print(f"Prompt Tokens: {callback_obj.prompt_tokens}")
    print(f"Completion Tokens: {callback_obj.completion_tokens}")
    print(f"Total Cost (USD): ${callback_obj.total_cost}")


@app.route('/rate', methods=["OPTIONS", "POST"])
def add_rating():
    if request.method == "OPTIONS":
        return make_response("", 204, headers_cors)

    id = request.json['id']
    rating = request.json['rating']

    add_rating(id, rating)

    return make_response("", 200, headers_cors)


@app.route('/qa', methods=["OPTIONS", "GET"])
def get_all_qa():
    if request.method == "OPTIONS":
        return make_response("", 204, headers_cors)

    QA = get_qa()

    return make_response(jsonify(QA), 200, headers_cors)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("8080"), debug=False)
