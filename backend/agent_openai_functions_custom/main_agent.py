from dotenv import load_dotenv

from langchain.chat_models.openai import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.agents import load_tools
import langchain

from tools.wiki_qa import wikiTool
from tools.ocean.stats import statsTool
from tools.ocean.token_balance import tokenbalanceTool
from tools.ocean.transactions import transactionsTool
from tools.ocean.utxo_balance import utxoTool
from tools.ocean.vaults import vaultsForAddressTool
from tools.ocean.vault import vaultInformationTool
from agent_openai_functions_custom.custom_functions_agent import (
    CustomOpenAIFunctionsAgent,
)

from langchain.agents import AgentExecutor, load_tools

load_dotenv()


def create_agent():
    print("🤖 Initializing main agent...")

    # Set debug to True to see A LOT of details of the agent's inner workings
    # langchain.debug = True
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613")

    tools = [
        wikiTool,
        statsTool,
        tokenbalanceTool,
        transactionsTool,
        utxoTool,
        vaultsForAddressTool,
        vaultInformationTool,
    ] + load_tools(["llm-math"], llm=llm)

    agent = CustomOpenAIFunctionsAgent.from_llm_and_tools(
        llm=llm,
        tools=tools,
        verbose=True,
    )

    main_agent_instance = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True
    )

    return main_agent_instance


if __name__ == "__main__":
    local_agent = create_agent()
    while True:
        question = input("Testing main agent: ")
        with get_openai_callback() as cb:
            response = local_agent(question)
            print(response)
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
