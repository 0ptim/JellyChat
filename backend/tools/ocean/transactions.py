from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_transactions(address: str, size: str) -> str:
    """Returns the transactions of an address."""
    requests = TextRequestsWrapper()
    return requests.get(f"https://ocean.defichain.com/v0/mainnet/address/{address}/transactions?size={size}")


def parsing_transaction(query: str) -> str:
    print("Query: ", query)
    address, size = query.split(",")
    print("Address: ", address, "Size: ", size)
    return get_transactions(address, int(size))


transactionTool = Tool(
    name="Get Transactions",
    description="To get the transactions of one specific address. The input to this tool should be in the format of 'address,size', where size is the amount of transactions needed.",
    func=parsing_transaction
)
