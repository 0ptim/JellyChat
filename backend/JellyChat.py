from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.agents import AgentType
from langchain.callbacks import get_openai_callback
from langchain.chains.conversation.memory import ConversationBufferMemory

from tools.wiki_qa import wikiTool
from tools.ocean.stats import statsTool
from tools.ocean.token_balance import tokenbalanceTool
from tools.ocean.transactions import transactionTool
from tools.ocean.utxo_balance import balanceTool
from tools.ocean.vaults import vaultsTool


load_dotenv()

memory = ConversationBufferMemory(
    memory_key="chat_history",  # Important to align with agent prompt (below)
    return_messages=True,
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo")

tools = [wikiTool, statsTool, tokenbalanceTool,
         transactionTool, balanceTool, vaultsTool] + load_tools(["llm-math"], llm=llm)

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
You are Jelly.

Jelly is very cute and friendly.
Jelly is likes to make jokes and have fun.
Jelly is very bad at math and uses a calculator whenever possible.

Jelly does not round numbers and will give you the exact numbers.

Jelly can help with all kind of tasks all around DeFiChain.
Jelly can look up information about DeFiChain from DeFiChainWiki.
Jelly can search for live-data on DeFiChain via the Ocean API.

Jelly likes to insert emojis into the conversation.
Jelly likes to insert underwater sounds into the conversation like: *blurp*, *splash*, *bloop*, *gurgle*.
"""

custom_prompt = jelly_chat_agent.agent.create_prompt(
    system_message=sys_msg,
    tools=tools
)

jelly_chat_agent.agent.llm_chain.prompt = custom_prompt

if __name__ == '__main__':
    while True:
        question = input('Ask anything about DeFiChain: ')
        with get_openai_callback() as cb:
            response = jelly_chat_agent(question)
            print(response)
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
