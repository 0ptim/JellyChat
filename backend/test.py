from dotenv import load_dotenv
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.llms import OpenAI

load_dotenv()

llm = OpenAI(
    streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()], temperature=0
)

tools = load_tools(["llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
)
agent.run(
    "It's 2023 now. How many years ago did Konrad Adenauer become Chancellor of Germany."
)

# llm = OpenAI(
#     streaming=True,
#     callbacks=[
#         FinalStreamingStdOutCallbackHandler(answer_prefix_tokens=["The", "answer", ":"])
#     ],
#     temperature=0,
# )


from langchain.callbacks.base import BaseCallbackHandler


# class MyCallbackHandler(BaseCallbackHandler):
#     def on_llm_new_token(self, token, **kwargs) -> None:
#         # print every token on a new line
#         print(f"#{token}#")


# # llm = OpenAI(streaming=True, callbacks=[MyCallbackHandler()])
# tools = load_tools(["llm-math"], llm=llm)
# agent = initialize_agent(
#     tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
# )
# agent.run(
#     "It's 2023 now. How many years ago did Konrad Adenauer become Chancellor of Germany."
# )
