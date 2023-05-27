import os
from flask import Flask
from flask_socketio import SocketIO
from data import SupabaseManager
from api_routes import setup_routes
from callback_handlers import CallbackHandlers
from dotenv import load_dotenv


class API:
    def __init__(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.after_request(self.cors_headers)
        self.socketio = SocketIO(
            self.app, async_mode="gevent", cors_allowed_origins="*"
        )
        self.manager = SupabaseManager()
        setup_routes(self)
        self.current_question = ""

    @staticmethod
    def cors_headers(response):
        response.headers.set("Access-Control-Allow-Origin", "*")
        response.headers.set("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.set("Access-Control-Allow-Headers", "API-Key, Content-Type")
        response.headers.set("Access-Control-Max-Age", "3600")
        return response

    @staticmethod
    def log_response_info(callback_obj):
        print(f"ℹ Total Tokens: {callback_obj.total_tokens}")
        print(f"ℹ Prompt Tokens: {callback_obj.prompt_tokens}")
        print(f"ℹ Completion Tokens: {callback_obj.completion_tokens}")
        print(f"ℹ Total Cost (USD): ${callback_obj.total_cost}")
