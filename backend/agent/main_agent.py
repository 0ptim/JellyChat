from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.agents import AgentExecutor, LLMSingleActionAgent, load_tools
from langchain.agents.conversational_chat.output_parser import ConvoOutputParser
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import LLMChain
import langchain

from tools.wiki_qa import wikiTool
from tools.ocean.stats import statsTool
from tools.ocean.token_balance import tokenbalanceTool
from tools.ocean.transactions import transactionsTool
from tools.ocean.utxo_balance import utxoTool
from tools.ocean.vaults import vaultsForAddressTool
from tools.ocean.vault import vaultInformationTool

from agent.prompt import PROMPT
from agent.promp_prep import CustomPromptTemplate


load_dotenv()


def create_agent(memory):
    print("🤖 Initializing main agent...")

    # Set debug to True to see A LOT of details of the agent's inner workings
    langchain.debug = True
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    tools = [
        wikiTool,
        statsTool,
        tokenbalanceTool,
        transactionsTool,
        utxoTool,
        vaultsForAddressTool,
        vaultInformationTool,
    ] + load_tools(["llm-math"], llm=llm)

    prompt = CustomPromptTemplate(
        template=PROMPT,
        tools=tools,
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps", "chat_history"],
    )

    output_parser = ConvoOutputParser()

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    tool_names = [tool.name for tool in tools]

    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names,
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True, memory=memory
    )

    return agent_executor


if __name__ == "__main__":
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )
    local_agent = create_agent(memory)
    while True:
        question = input("Testing main agent: ")
        with get_openai_callback() as cb:
            response = local_agent(question)
            print(response)
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")
