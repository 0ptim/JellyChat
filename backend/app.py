from dotenv import load_dotenv
from flask import Flask, jsonify, request, make_response
from langchain.callbacks import get_openai_callback

from data import init_db, add_rating, add_qa, get_qa
from JellyChat import create_jelly_chat_agent

load_dotenv()

app = Flask(__name__)


with app.app_context():
    init_db()


agents_by_user = {}


def agent_for_user(user_token):
    jelly_chat_agent = agents_by_user.get(user_token)

    if jelly_chat_agent is None:
        jelly_chat_agent = create_jelly_chat_agent()
        agents_by_user[user_token] = jelly_chat_agent

    return jelly_chat_agent


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

    user_token = request.json.get('user_token', '').strip()
    if not user_token:
        return jsonify({'error': 'User token is required'}), 400

    jelly_chat_agent = agent_for_user(user_token)

    question: str = ""
    if request.is_json and 'question' in request.json:
        question = request.json["question"].strip()
        print("Question asked:", question)

    if question == "":
        return make_response("No question provided", 400)

    with get_openai_callback() as cb:
        responseObj = jelly_chat_agent(question)
        print("🔥 Response object:", responseObj)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

    response = responseObj["output"].strip()

    print("❤ Respone", response)

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
