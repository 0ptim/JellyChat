from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_tokenbalance(query: str) -> str:
    """Returns the token balance of an address."""
    requests = TextRequestsWrapper()
    return requests.get(f"https://ocean.defichain.com/v0/mainnet/address/{query}/tokens")


description = """
To get the token balance of one specific address.
Provide the address as input.
"""

tokenbalanceTool = Tool(
    name="Get Token Balance",
    description=description,
    func=get_tokenbalance
)
