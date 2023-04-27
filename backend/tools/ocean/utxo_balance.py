from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_balance(query: str) -> str:
    """Returns the UTXO balance of an address."""
    requests = TextRequestsWrapper()
    return requests.get(f"https://ocean.defichain.com/v0/mainnet/address/{query}/balance")


description = """
To get the UTXO balance of one specific address. Please provide the address as input.
"""

balanceTool = Tool(
    name="Get UTXO Balance",
    description=description,
    func=get_balance
)
