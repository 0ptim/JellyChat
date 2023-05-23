# Imports
from typing import Any, Dict
from dotenv import load_dotenv
from flask import Flask, jsonify, request, make_response
from flask_socketio import SocketIO, emit
from langchain.callbacks import get_openai_callback
from langchain.callbacks.base import BaseCallbackHandler
from session_agents import agent_for_user
from data import SupabaseManager
from functools import wraps


# Setup
load_dotenv()
app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

manager = SupabaseManager()


def cors_headers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.set('Access-Control-Allow-Headers',
                             'API-Key, Content-Type')
        response.headers.set('Access-Control-Max-Age', '3600')
        return response

    return decorated_function


class CustomHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        """ Emit the action name to the client, so the user can see what the agent is doing."""
        print(f"🔥 Tool started: {serialized}")
        tool_message = get_tool_message(serialized["name"])
        emit("tool_start", {"tool_name": tool_message})
        # Yield control back to the caller, so the client can receive the event instantly.
        socketio.sleep(0)


def get_tool_message(name: str) -> str:
    """depending on the tool name, return a message to the user"""
    if name == "DeFiChainWiki QA System":
        return "I'll go look this up in the DeFiChainWiki for you 🔎"
    elif name == "Get Stats":
        return "Let me gather the latest blockchain statistics for you 📊"
    elif name == "Get Token Balance":
        return "Checking the token balance now ⚖️"
    elif name == "Get Transactions":
        return "Fetching the transaction history 🔄"
    elif name == "Get UTXO Balance":
        return "Let's check the UTXO balance 💱"
    elif name == "Get Vaults for Address":
        return "Analyzing vaults associated with the address 🏦"
    elif name == "Get Vault Information":
        return "Retrieving detailed vault information ℹ️"
    elif name == "Calculator":
        return "Let's do the math together 🧮"
    else:
        raise ValueError(f"Unknown tool name: {name}")


def log_response_info(response_obj, callback_obj):
    print(f"🔥 Response object: {response_obj}")
    print(f"Total Tokens: {callback_obj.total_tokens}")
    print(f"Prompt Tokens: {callback_obj.prompt_tokens}")
    print(f"Completion Tokens: {callback_obj.completion_tokens}")
    print(f"Total Cost (USD): ${callback_obj.total_cost}")


def extract_data(json_request, field):
    return json_request.get(field, "").strip()


@socketio.on("user_message")
def process_input(user_token, message):
    if not user_token:
        emit("error", {"error": "User token is required"})
        return

    if not message:
        emit("error", {"error": "Input is required"})
        return

    chat_agent = agent_for_user(user_token)

    with get_openai_callback() as cb:
        response_obj = chat_agent(
            message, callbacks=[CustomHandler()])
        log_response_info(response_obj, cb)

    response = response_obj["output"].strip()
    manager.add_message_response(message, response)

    emit("final_message", {"message": response})


@app.route("/user_message", methods=["OPTIONS", "POST"])
@cors_headers
def process_input():
    if request.method == "OPTIONS":
        return make_response("", 204)

    if not request.is_json:
        return make_response("Request should be in JSON format", 400)

    user_token = extract_data(request.json, "user_token")
    if not user_token:
        return jsonify({"error": "User token is required"}), 400

    message = extract_data(request.json, "message")
    if not message:
        return jsonify({"error": "Message is required"}), 400

    chat_agent = agent_for_user(user_token)

    with get_openai_callback() as cb:
        response_obj = chat_agent(message)
        log_response_info(response_obj, cb)

    response = response_obj["output"].strip()
    manager.add_message_response(message, response)

    return make_response(jsonify({"response": response}), 200)


@app.route('/messages_answers', methods=["OPTIONS", "GET"])
def get_all_messages_answers():
    if request.method == "OPTIONS":
        return make_response("", 204)

    messages_answers = manager.get_messages_answers()

    return make_response(jsonify(messages_answers), 200)


if __name__ == "__main__":
    print("🚀 Starting server...")
    socketio.run(app, host="0.0.0.0", port=8080)
