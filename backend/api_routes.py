from flask import jsonify, request, make_response
from session_agents import agent_for_user
from langchain.callbacks import get_openai_callback
from callback_handlers import CallbackHandlers
from flask_socketio import emit


def _is_valid_input(user_token, message):
    if not user_token:
        return False, jsonify({"error": "User token is required"}), 400
    if not message:
        return False, jsonify({"error": "Message is required"}), 400
    return True, None, None


def process_input(app_instance, user_token, message):
    is_valid, error_response, error_code = _is_valid_input(user_token, message)
    if not is_valid:
        return error_response, error_code

    chat_agent = agent_for_user(user_token)

    with get_openai_callback() as cb:
        response_obj = chat_agent(
            message,
            callbacks=[
                CallbackHandlers.QAToolHandler(app_instance),
                CallbackHandlers.ToolUseNotifier(app_instance),
            ],
        )
        app_instance.log_response_info(cb)

    response = response_obj["output"].strip()

    return make_response(jsonify({"response": response}), 200)


def setup_routes(app_instance):
    app = app_instance.app
    socketio = app_instance.socketio

    @socketio.on("user_message")
    def process_input_socket(user_token, message):
        is_valid, error_response, error_code = _is_valid_input(user_token, message)
        if not is_valid:
            emit("error", error_response.get_json())
            return

        response, _ = process_input(app_instance, user_token, message)
        emit("final_message", {"message": response.get_json()["response"]})

    @app.route("/user_message", methods=["POST"])
    def process_input_rest():
        if not request.is_json:
            return make_response("Request should be in JSON format", 400)

        user_token = request.json.get("user_token", "").strip()
        message = request.json.get("message", "").strip()

        return process_input(app_instance, user_token, message)

    @app.route("/messages_answers", methods=["GET"])
    def get_all_messages_answers():
        messages_answers = app_instance.manager.get_question_answers()
        return make_response(jsonify(messages_answers), 200)

    @app.after_request
    def handle_options_requests(response):
        if request.method == "OPTIONS":
            response.status_code = 204
        return response
