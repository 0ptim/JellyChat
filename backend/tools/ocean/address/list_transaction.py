from langchain.agents import Tool

from ..utils import getOcean, Network

def list_transaction(address: str, size: str) -> str:
    """Returns the transactions of an address."""
    return getOcean().address.listTransaction(address=address, size=size)


def parsing_list_transaction(query: str) -> str:
    print("Query: ", query)
    address, size = query.split(",")
    print("Address: ", address, "Size: ", size)
    return list_transaction(address, int(size))


description = """
To get the transactions of one specific address.
The input to this tool should be in the format of 'address,size', where size is the amount of transactions needed. Example: df1...,10
"""

addressListTransactionsTool = Tool(
    name="Get Transactions",
    description=description,
    func=parsing_list_transaction
)
