from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.agents import AgentType

from tools.wiki_qa import wikiTool
from tools.ocean.stats import statsTool
from tools.ocean.token_balance import tokenbalanceTool
from tools.ocean.transactions import transactionTool
from tools.ocean.utxo_balance import balanceTool
from tools.ocean.vaults import vaultsTool


load_dotenv()


llm = OpenAI(temperature=0, model_name="text-davinci-003")

tools = [wikiTool, statsTool, tokenbalanceTool,
         transactionTool, balanceTool, vaultsTool] + load_tools(["llm-math"], llm=llm)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=8)

while True:
    question = input('Ask anything about DeFiChain: ')
    response = agent.run(question)
    print(response)
