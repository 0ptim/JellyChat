from langchain.agents import Tool

from ..utils import getOcean, Network


def list_transaction_unspent(query: str) -> str:
    """List all unspent inputs belonging to an address"""
    return getOcean().address.listTransactionUnspent(query)


description = """
List all unspent inputs belonging to an address
Return information: id: str, hid: str, sort: str, block: (hash: str, height: int, time: int, medianTime: int), 
script: (type: str, hex: str), vout: (txid: str, n: int, value: str, tokenId: int)
Provides a address as an input.
The input has to ba a string.
"""

addressListTransactionUnspentTool = Tool(
    name="List Unspent Inputs of Address",
    description=description,
    func=list_transaction_unspent
)
