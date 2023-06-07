from langchain.agents import Tool

from ..utils import getOcean, Network


def list_transaction(query: str) -> str:
    """Returns the transactions of an address."""
    address, size = query.split(",")
    return getOcean().address.listTransaction(address=address, size=size)


description = """
Lists transaction belonging to the specified address
Return information: id: str, hid: str, type: ‘vin’ | ‘vout’, typeHex: ‘00’ | ‘01’, txid: str, block: (hash: str, 
height: int, time: int, medianTime: int), script: (type: str, hex: str), vin: (txid: str, n: int), 
vout: (txid: str, n: int), value: str, tokenId: int
Provides a address and an number of transactions as an input. If no number is provided use  as default.
The input has to be formatted like this: address,number 
"""

addressListTransactionsTool = Tool(
    name="Get Address Transactions",
    description=description,
    func=list_transaction
)
