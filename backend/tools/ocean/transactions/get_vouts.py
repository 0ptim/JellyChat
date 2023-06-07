from langchain.agents import Tool

from ..utils import getOcean, Network


def get_vouts(query: str) -> str:
    """Get a list of vouts of a Transaction"""
    return getOcean().transactions.getVouts(query, size=200)


description = """
Gets a list of outputs of a transaction with specified txid
Information: id: str, txid: str, n: int, value: str, tokenId: int, script: (hex: str, type: str)
Provides the txid of the transaction as an input.
Only an txid is allowed as a identification of the transaction.
The input has to be a string.
"""

transactionGetVoutsTool = Tool(
    name="Get Outputs Of Transaction",
    description=description,
    func=get_vouts
)
