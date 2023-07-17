from asyncio import Event, Queue
import json
from typing import Any, Dict, Generator, List, Optional
from langchain.callbacks.base import BaseCallbackHandler
from flask_socketio import emit
from utils import get_tool_message
from data import add_question_answer, add_chat_message
from tools.wiki_qa import wikiTool
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import LLMResult
from langchain.callbacks.streaming_aiter_final_only import DEFAULT_ANSWER_PREFIX_TOKENS


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

    class FinalOutputHandler(StreamingStdOutCallbackHandler):
        """Callback handler for streaming in agents.
        Only works with agents using LLMs that support streaming.
        Only the final output of the agent will be streamed.
        """

        def __init__(
            self,
            *,
            answer_prefix_tokens: Optional[List[str]] = None,
            strip_tokens: bool = True,
            stream_prefix: bool = False,
        ) -> None:
            super().__init__()
            if answer_prefix_tokens is None:
                self.answer_prefix_tokens = DEFAULT_ANSWER_PREFIX_TOKENS
            else:
                self.answer_prefix_tokens = answer_prefix_tokens
            if strip_tokens:
                self.answer_prefix_tokens_stripped = [
                    token.strip() for token in self.answer_prefix_tokens
                ]
            else:
                self.answer_prefix_tokens_stripped = self.answer_prefix_tokens
            self.last_tokens = [""] * len(self.answer_prefix_tokens)
            self.last_tokens_stripped = [""] * len(self.answer_prefix_tokens)
            self.strip_tokens = strip_tokens
            self.stream_prefix = stream_prefix
            self.answer_reached = False
            self._token_queue: Queue = Queue()

        def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
            """Run when LLM ends running. Stream the final output to the frontend"""
            print("\n\n")
            print("LLM Final Response: ", response)
            print("\n\n")
