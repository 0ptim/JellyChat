from langchain.agents import Tool

from ..utils import getOcean, Network


def get_balance(query: str) -> str:
    """Returns the UTXO balance of an address."""
    return getOcean().address.getBalance(query)


description = """
Gets the current DFI utxo balance of a specific address.
Return information: float
Provides a address as an input.
The input has to be a string.
"""

addressGetBalanceTool = Tool(
    name="get_utxo_balance",
    description=description,
    func=get_balance
)
