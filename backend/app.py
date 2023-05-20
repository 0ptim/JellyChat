# Imports
from typing import Any, Dict
from dotenv import load_dotenv
from flask import Flask, jsonify, request, make_response
from flask_socketio import SocketIO, emit
from langchain.callbacks import get_openai_callback
from langchain.callbacks.base import BaseCallbackHandler
from session_agents import agent_for_user
from data import SupabaseManager


# Setup
load_dotenv()
app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

manager = SupabaseManager()


class CustomHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        """ Emit the action name to the client, so the user can see what jellychat is doing."""
        emit("tool_start", {"tool_name": serialized["name"]})


@socketio.on("user_input")
def process_question(question, user_token):
    if not user_token:
        emit("error", {"error": "User token is required"})
        return

    if not question:
        emit("error", {"error": "Question is required"})
        return

    jelly_chat_agent = agent_for_user(user_token)

    with get_openai_callback() as cb:
        response_obj = jelly_chat_agent(
            question, callbacks=[CustomHandler()])
        log_response_info(response_obj, cb)

    response = response_obj["output"].strip()
    manager.add_qa(question, response)

    emit("final_message", {"message": response})


def log_response_info(response_obj, callback_obj):
    print(f"🔥 Response object: {response_obj}")
    print(f"Total Tokens: {callback_obj.total_tokens}")
    print(f"Prompt Tokens: {callback_obj.prompt_tokens}")
    print(f"Completion Tokens: {callback_obj.completion_tokens}")
    print(f"Total Cost (USD): ${callback_obj.total_cost}")


@app.route('/qa', methods=["OPTIONS", "GET"])
def get_all_qa():
    if request.method == "OPTIONS":
        return make_response("", 204)

    QA = manager.get_qa()

    return make_response(jsonify(QA), 200)


if __name__ == "__main__":
    print("🚀 Starting server...")
    socketio.run(app, host="0.0.0.0", port=8080)
