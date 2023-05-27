from typing import Any, Dict
from flask import Flask, request
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from data import SupabaseManager
from session_agents import agent_for_user
from langchain.callbacks import get_openai_callback
from langchain.callbacks.base import BaseCallbackHandler
from flask import Flask, jsonify, request, make_response
from functools import wraps


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


class ToolUseNotifier(BaseCallbackHandler):
    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        """ Emit the action name to the client, so the user can see what the agent is doing."""
        tool_message = get_tool_message(serialized["name"])
        emit("tool_start", {"tool_name": tool_message})
        # Yield control back to the caller, so the client can receive the event instantly.
        self.app_instance.socketio.sleep(0)


class QAToolHandler(BaseCallbackHandler):
    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        """When the QA starts, save the question to a temporary field."""
        if serialized["name"] == "DeFiChainWiki QA System":
            print(f"🔥 QA Tool started: {input_str}")
            self.current_question = input_str

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """When the QA tool ends, save the question and answer to the database."""
        if self.current_question:
            print(f"⭕ QA Tool ended: {output}")
            self.app_instance.manager.add_question_answer(
                self.current_question, output)
            # Reset the current question.
            self.current_question = ""


class API:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.socketio = SocketIO(
            self.app, async_mode='gevent', cors_allowed_origins="*")
        self.manager = SupabaseManager()
        self.setup_routes()
        self.current_question = ""

    def extract_data(self, json_request, field):
        return json_request.get(field, "").strip()

    def cors_headers(self, f):
        @ wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)
            response.headers.set('Access-Control-Allow-Origin', '*')
            response.headers.set(
                'Access-Control-Allow-Methods', 'POST, OPTIONS')
            response.headers.set('Access-Control-Allow-Headers',
                                 'API-Key, Content-Type')
            response.headers.set('Access-Control-Max-Age', '3600')
            return response

        return decorated_function

    def setup_routes(self):
        @ self.socketio.on("user_message")
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
                    message, callbacks=[QAToolHandler(self), ToolUseNotifier(self)])
                self.log_response_info(response_obj, cb)

            response = response_obj["output"].strip()

            emit("final_message", {"message": response})

        @ self.app.route("/user_message", methods=["OPTIONS", "POST"])
        @ self.cors_headers
        def process_input():
            if request.method == "OPTIONS":
                return make_response("", 204)

            if not request.is_json:
                return make_response("Request should be in JSON format", 400)

            user_token = self.extract_data(request.json, "user_token")
            if not user_token:
                return jsonify({"error": "User token is required"}), 400

            message = self.extract_data(request.json, "message")
            if not message:
                return jsonify({"error": "Message is required"}), 400

            chat_agent = agent_for_user(user_token)

            with get_openai_callback() as cb:
                response_obj = chat_agent(
                    message, callbacks=[QAToolHandler(self)])
                self.log_response_info(cb)

            response = response_obj["output"].strip()

            return make_response(jsonify({"response": response}), 200)

        @ self.app.route('/messages_answers', methods=["OPTIONS", "GET"])
        def get_all_messages_answers():
            if request.method == "OPTIONS":
                return make_response("", 204)

            messages_answers = self.manager.get_question_answers()

            return make_response(jsonify(messages_answers), 200)

    def log_response_info(self, callback_obj):
        print(f"ℹ Total Tokens: {callback_obj.total_tokens}")
        print(f"ℹ Prompt Tokens: {callback_obj.prompt_tokens}")
        print(f"ℹ Completion Tokens: {callback_obj.completion_tokens}")
        print(f"ℹ Total Cost (USD): ${callback_obj.total_cost}")
