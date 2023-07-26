from flask import jsonify, request, make_response
from session_agents import agent_for_user
from langchain.callbacks import get_openai_callback
from callback_handlers import CallbackHandlers
from flask_socketio import emit
from data import (
    check_user_exists,
    create_user,
    get_chat_history,
    get_question_answers,
    add_chat_message,
)


def _is_valid_input(user_token, message, application):
    if not user_token:
        return False, jsonify({"error": "User token is required"}), 400
    if not message:
        return False, jsonify({"error": "Message is required"}), 400
    if not application:
        return False, jsonify({"error": "Application is required"}), 400

    return True, None, None


def process_input(app_instance, user_token, message, application):
    is_valid, error_response, error_code = _is_valid_input(
        user_token, message, application
    )
    if not is_valid:
        return error_response, error_code

    user_id = get_user_id(user_token)

    chat_agent = agent_for_user(
        user_token, CallbackHandlers.FinalOutputHandler(app_instance)
    )

    add_chat_message(user_id, "human", message, application=application)

    with get_openai_callback() as cb:
        response_obj = chat_agent(
            message,
            callbacks=[
                CallbackHandlers.ToolUseNotifier(app_instance, user_id),
                CallbackHandlers.QAToolHandler(app_instance),
            ],
        )
        log_response_info(cb)

    response = response_obj["output"].strip()

    add_chat_message(user_id, "jelly", response)

    return jsonify({"response": response}), 200


def get_user_id(user_token):
    """
    Get the user_id for a user_token. If the user does not exist, create a new user.
    """
    user_id = check_user_exists(user_token)
    if user_id is None:
        print("Creating user: ", user_token)
        user_id = create_user(user_token)
        set_inital_message(user_id)
    return user_id


def set_inital_message(user_id):
    """
    Set the initial message from Jelly as greeting.
    """
    add_chat_message(
        user_id,
        "jelly",
        """Hi there, it's Jelly 🪼

Your friendly undersea guide to everything DeFiChain. Feel comfortable to dive into any question you've got.

Ready to navigate through this exciting blockchain journey together? 🌊""",
    )


def log_response_info(callback_obj):
    print(f"ℹ Total Tokens: {callback_obj.total_tokens}")
    print(f"ℹ Prompt Tokens: {callback_obj.prompt_tokens}")
    print(f"ℹ Completion Tokens: {callback_obj.completion_tokens}")
    print(f"ℹ Total Cost (USD): ${callback_obj.total_cost}")


def setup_routes(app_instance):
    app = app_instance.app
    socketio = app_instance.socketio

    @socketio.on("user_message")
    def process_input_socket(user_token, message, application):
        try:
            is_valid, error_response, error_code = _is_valid_input(
                user_token, message, application
            )
            if not is_valid:
                emit("error", error_response.get_json())
                return

            response, status_code = process_input(
                app_instance, user_token, message, application
            )
            emit("final_message", {"message": response.get_json()["response"]})
        except Exception as e:
            print(e)
            emit(
                "final_message",
                {
                    "message": "Yikes! 🌊 I made a bubbly blunder. Please accept this humble jellyfish's apologies for the inconvenience. 💜 Can we swim forward and try again together? 🐙"
                },
            )

    @app.route("/user_message", methods=["POST"])
    def process_input_rest():
        try:
            if not request.is_json:
                return make_response("Request should be in JSON format", 400)

            user_token = request.json.get("user_token", "").strip()
            message = request.json.get("message", "").strip()
            application = request.json.get("application", "").strip()

            response, status_code = process_input(
                app_instance, user_token, message, application
            )
            return make_response(response, status_code)
        except Exception as e:
            print(e)
            custom_message = "Yikes! 🌊 I made a bubbly blunder. Please accept this humble jellyfish's apologies for the inconvenience. 💜 Can we swim forward and try again together? 🐙"
            return make_response(custom_message, 500)

    @app.route("/history", methods=["POST"])
    def get_user_history():
        try:
            user_token = request.json.get("user_token", "")
            if not user_token:
                return make_response("User token is missing or empty", 400)

            user_id = get_user_id(user_token)

            chat_messages = get_chat_history(user_id)
            return make_response(jsonify(chat_messages), 200)
        except Exception:
            return make_response("Exception while getting history", 500)

    @app.route("/messages_answers", methods=["GET"])
    def get_all_messages_answers():
        messages_answers = get_question_answers()
        return make_response(jsonify(messages_answers), 200)

    @app.after_request
    def handle_options_requests(response):
        if request.method == "OPTIONS":
            response.status_code = 204
        return response
