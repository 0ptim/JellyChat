from langchain.agents import Tool

from ..utils import getOcean, Network


def get_balance(query: str) -> str:
    """Returns the UTXO balance of an address."""
    return getOcean().address.getBalance(query)


description = """
To get the UTXO balance of one specific address.
Provide the address as input. Example: df1...
"""

addressGetBalanceTool = Tool(
    name="Get UTXO Balance",
    description=description,
    func=get_balance
)
