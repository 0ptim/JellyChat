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
