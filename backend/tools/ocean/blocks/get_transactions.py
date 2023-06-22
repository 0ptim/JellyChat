from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def get_transactions(query: str) -> str:
    """Gets all transactions within a block"""
    hash, size = query.split(",")

    return getOcean().blocks.getTransactions(hash, size)


description = """
Returns all transactions within a block and their corresponding information.
Return Information: id: str, order: int, block: (hash: str, height: int, time: int, medianTime: int), txid: str, 
hash: str, version: int, size: int, vSize: int, weight: int, lockTime: int, vinCount: int, voutCount: int, 
totalVoutValue: str
Takes the blockhash and a number of transactions (blockhash, number) as an input. Seperated by comma.
The input has to be a string. 
"""

blocksGetTransactionsTool = Tool(
    name="get_transactions",
    description=description,
    func=get_transactions
)
