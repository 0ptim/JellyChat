import json
from langchain.callbacks.base import BaseCallbackHandler
from flask_socketio import emit
from utils import get_tool_message
from data import add_question_answer, add_chat_message
from tools.wiki_qa import wikiTool


class CallbackHandlers:
    class ToolUseNotifier(BaseCallbackHandler):
        def __init__(self, app_instance, user_id):
            super().__init__()
            self.app_instance = app_instance
            self.user_id = user_id

        def on_tool_start(self, serialized, input_str, **kwargs):
            """
            Notify the user that a tool has started
            Saves the tool message to the database
            """
            print(f"🔥 Tool started: {serialized['name']}")
            tool_message = get_tool_message(serialized["name"])

            add_chat_message(self.user_id, "tool", tool_message)

            emit("tool_start", {"tool_name": tool_message})
            self.app_instance.socketio.sleep(0)

    class QAToolHandler(BaseCallbackHandler):
        def __init__(self, app_instance):
            super().__init__()
            self.app_instance = app_instance
            self.current_question = ""

        def on_tool_start(self, serialized, input_str, **kwargs):
            if serialized["name"] == wikiTool.name:
                input_dict = json.loads(input_str.replace("'", '"'))
                question = input_dict["arg1"]
                print(f"QA Tool started: {question}")
                self.current_question = question

        def on_tool_end(self, output, **kwargs):
            if self.current_question:
                print(f"QA Tool ended: {output}")
                add_question_answer(self.current_question, output)
                self.current_question = ""

    class FinalOutputHandler(BaseCallbackHandler):
        print("FinalOutputHandler")

        ignore_chat_model = True

        def on_llm_new_token(self, token: str, **kwargs) -> None:
            """
            ASDF
            """
            print(f"My custom handler, token: {token}")
