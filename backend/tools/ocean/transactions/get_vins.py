from langchain.agents import Tool

from ..utils import getOcean, Network


def get_vins(query: str) -> str:
    """Get a list of vins of a Transaction"""
    return getOcean().transactions.getVins(query, size=200)


description = """
Gets a list of inputs of a transaction with specified txid
Information: id: str, txid: str, coinbase: str, vout: (id: str, txid: str, n: int, value: str, tokenId: int, 
script: (hex: str)), script: (hex: str), txInWitness: str[], sequence: str
Provides the txid of the transaction as an input.
Only an txid is allowed as a identification of the transaction.
The input has to be a string.
"""

transactionGetVinsTool = Tool(
    name="get_inputs_of_transaction",
    description=description,
    func=get_vins
)
