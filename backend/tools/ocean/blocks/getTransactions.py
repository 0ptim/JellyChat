from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def getTransactions(query: str) -> str:
    """Gets all transactions within a block"""
    hash, size = query.split(",")

    if int(size) > 4:
        size = 4

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
    name="Get Transactions",
    description=description,
    func=getTransactions
)
