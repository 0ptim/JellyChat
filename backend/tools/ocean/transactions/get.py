from langchain.agents import Tool

from ..utils import getOcean, Network


def get(query: str) -> str:
    """Get a Transaction"""
    return getOcean().transactions.get(query)


description = """
Gets information about the transaction of the specified txid
Information: id: str, order: int, block: (hash: str, height: int, time: int, medianTime: int), txid: str, hash: str, 
version: int, size: int, vSize: int, weight: int, lockTime: int, vinCount: int, voutCount: int, totalVoutValue: str
Provides the txid of the transaction as an input.
Only an txid is allowed as a identification of the transaction.
The input has to be a string.
"""

transactionGetTool = Tool(
    name="get_transaction",
    description=description,
    func=get
)
