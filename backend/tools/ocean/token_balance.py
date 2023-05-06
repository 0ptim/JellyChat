from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool

from . import getOcean, Network


def get_tokenbalance(query: str) -> str:
    """Returns the token balance of an address."""
    return getOcean().address.listToken(query)


description = """
To get the token balance of one specific address.
Provide the address as input. Example: df1...
"""

tokenbalanceTool = Tool(
    name="Get Token Balance",
    description=description,
    func=get_tokenbalance
)
