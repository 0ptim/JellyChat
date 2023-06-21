from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from api_routes import setup_routes
from dotenv import load_dotenv


class API:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)
        CORS(self.app)
        self.socketio = SocketIO(
            self.app, async_mode="gevent", cors_allowed_origins="*"
        )
        setup_routes(self)
        self.current_question = ""

    @staticmethod
    def log_response_info(callback_obj):
        print(f"ℹ Total Tokens: {callback_obj.total_tokens}")
        print(f"ℹ Prompt Tokens: {callback_obj.prompt_tokens}")
        print(f"ℹ Completion Tokens: {callback_obj.completion_tokens}")
        print(f"ℹ Total Cost (USD): ${callback_obj.total_cost}")
