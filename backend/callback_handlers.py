from langchain.callbacks.base import BaseCallbackHandler
from flask_socketio import emit
from utils import get_tool_message
from data import add_question_answer, add_chat_message


class CallbackHandlers:
    class ToolUseNotifier(BaseCallbackHandler):
        def __init__(self, app_instance, user_id):
            super().__init__()
            self.app_instance = app_instance
            self.user_id = user_id

        def on_tool_start(self, serialized, input_str, **kwargs):
            tool_message = get_tool_message(serialized["name"])

            add_chat_message(self.user_id, "ai", tool_message)

            emit("tool_start", {"tool_name": tool_message})
            self.app_instance.socketio.sleep(0)

    class QAToolHandler(BaseCallbackHandler):
        def __init__(self, app_instance):
            super().__init__()
            self.app_instance = app_instance

        def on_tool_start(self, serialized, input_str, **kwargs):
            if serialized["name"] == "DeFiChainWiki QA System":
                print(f"🔥 QA Tool started: {input_str}")
                self.current_question = input_str

        def on_tool_end(self, output, **kwargs):
            if self.current_question:
                print(f"⭕ QA Tool ended: {output}")
                add_question_answer(self.current_question, output)
                self.current_question = ""
