from langchain.agents import Tool

from ..utils import getOcean, Network


def list_token(query: str) -> str:
    """Returns the token balance of an address."""
    return getOcean().address.listToken(query)


description = """
To get the token balance of one specific address.
Provide the address as input. Example: df1...
"""

addressListTokenTool = Tool(
    name="Get Token Balance",
    description=description,
    func=list_token
)
