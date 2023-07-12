from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.callbacks import get_openai_callback
from langchain.agents import AgentType, load_tools, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferMemory
import langchain

from tools.wiki_qa import wikiTool
from tools.ocean import oceanTools

load_dotenv()


def create_agent(memory):
    print("🤖 Initializing main agent...")

    # Set debug to True to see A LOT of details of the agent's inner workings
    # langchain.debug = True
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k-0613", temperature=0.7)

    tools = [wikiTool] + load_tools(["llm-math"], llm=llm) + oceanTools

    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    }

    open_ai_agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs=agent_kwargs,
        memory=memory,
        max_iterations=4,
        early_stopping_method="generate",
    )

    return open_ai_agent


if __name__ == "__main__":
    memory = ConversationBufferMemory(
        memory_key="memory",
        return_messages=True,
    )
    local_agent = create_agent(memory)
    while True:
        question = input("⚡ Testing main agent: ")
        with get_openai_callback() as cb:
            response = local_agent(question)
            print(response)
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
