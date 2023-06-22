from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def send(query: str) -> [{}]:
    """Send a raw transaction"""
    try:
        return getOcean().rawTx.send(query)
    except Exception as e:
        return e


description = """
Sends the provided raw transaction to the network
Return Information: txid of the submitted transaction
Provides a raw transaction (hex string) as an input.
The input has to be a string. 
"""

rawTxSendTool = Tool(
    name="send_raw_transaction",
    description=description,
    func=send
)
