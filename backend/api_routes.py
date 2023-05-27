from flask import jsonify, request, make_response
from flask import jsonify, request, make_response
from session_agents import agent_for_user
from langchain.callbacks import get_openai_callback
from callback_handlers import CallbackHandlers
from flask_socketio import emit


def process_input(app_instance):
    user_token = request.json.get("user_token", "").strip()
    message = request.json.get("message", "").strip()

    if not user_token:
        return jsonify({"error": "User token is required"}), 400

    if not message:
        return jsonify({"error": "Message is required"}), 400

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
        if not user_token:
            emit("error", {"error": "User token is required"})
            return

        if not message:
            emit("error", {"error": "Input is required"})
            return

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

        emit("final_message", {"message": response})

    @app.route("/user_message", methods=["OPTIONS", "POST"])
    def process_input_rest():
        if request.method == "OPTIONS":
            return make_response("", 204)

        if not request.is_json:
            return make_response("Request should be in JSON format", 400)

        return process_input(app_instance)

    @app.route("/messages_answers", methods=["OPTIONS", "GET"])
    def get_all_messages_answers():
        if request.method == "OPTIONS":
            return make_response("", 204)

        messages_answers = app_instance.manager.get_question_answers()

        return make_response(jsonify(messages_answers), 200)
