from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool

from . import getOcean, Network

def get_transactions(address: str, size: str) -> str:
    """Returns the transactions of an address."""
    return getOcean().address.listTransaction(address=address, size=size)


def parsing_transaction(query: str) -> str:
    print("Query: ", query)
    address, size = query.split(",")
    print("Address: ", address, "Size: ", size)
    return get_transactions(address, int(size))


description = """
To get the transactions of one specific address.
The input to this tool should be in the format of 'address,size', where size is the amount of transactions needed. Example: df1...,10
"""

transactionsTool = Tool(
    name="Get Transactions",
    description=description,
    func=parsing_transaction
)
