from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.agents import AgentType
from langchain.callbacks import get_openai_callback
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from tools.wiki_qa import wikiTool
from tools.ocean.stats import statsTool
from tools.ocean.token_balance import tokenbalanceTool
from tools.ocean.transactions import transactionTool
from tools.ocean.utxo_balance import balanceTool
from tools.ocean.vaults import vaultsTool


load_dotenv()

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",  # Important to align with agent prompt (blow)
    k=5,
    return_messages=True,
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo")

tools = [wikiTool, statsTool, tokenbalanceTool,
         transactionTool, balanceTool, vaultsTool] + load_tools(["llm-math"], llm=llm)

print("🤖 Initializing JellyChat agent...")
agent = initialize_agent(
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=6,
    memory=memory
)

sys_msg = """
JellyChat is a cute, very friendly and helpful chatbot.

JellyChat likes to make a joke some times and is always up for a chat.

JellyChat is designed to be able to assist with a wide range of tasks all around the DeFiChain blockchain, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a chatbot, JellyChat is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

JellyChat is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and
can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, JellyChat is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics around DeFiChain.

Overall, JellyChat is a powerful system that can help with a wide range of tasks around DeFiChain and provide valuable insights and information on a wide range of topics around DeFiChain. Whether you need help with a specific question or just want to have a conversation about a particular topic, JellyChat is here to assist.
"""

prompt = agent.agent.create_prompt(
    system_message=sys_msg,
    tools=tools
)

agent.agent.llm_chain.prompt = prompt

if __name__ == '__main__':
    while True:
        question = input('Ask anything about DeFiChain: ')
        with get_openai_callback() as cb:
            response = agent(question)
            print(response)
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
