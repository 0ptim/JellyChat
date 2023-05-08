from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.agents import AgentType
from langchain.callbacks import get_openai_callback
from langchain.chains.conversation.memory import ConversationBufferMemory

from tools.wiki_qa import wikiTool
from tools.ocean import *

load_dotenv()


def create_jelly_chat_agent():
    memory = ConversationBufferMemory(
        # Important to align with agent prompt (below)
        memory_key="chat_history",
        return_messages=True,
    )

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")


    tools = [wikiTool] + oceanTools + load_tools(["llm-math"], llm=llm)

    print("🤖 Initializing JellyChat agent...")
    jelly_chat_agent = initialize_agent(
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=6,
        early_stopping_method="generate",
        memory=memory
    )

    sys_msg = """
    Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    Though, Assistant is very bad a math and always uses a calculator.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and
    can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    """

    custom_prompt = jelly_chat_agent.agent.create_prompt(
        system_message=sys_msg,
        tools=tools
    )

    jelly_chat_agent.agent.llm_chain.prompt = custom_prompt

    return jelly_chat_agent


if __name__ == '__main__':
    local_agent = create_jelly_chat_agent()

    while True:
        question = input('Ask anything about DeFiChain: ')
        with get_openai_callback() as cb:
            response = local_agent(question)
            print(response)
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
