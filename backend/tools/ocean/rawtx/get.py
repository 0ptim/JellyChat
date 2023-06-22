from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def get(query: str) -> [{}]:
    """Get a raw transaction"""
    return getOcean().rawTx.get(query)


description = """
Returns the raw transaction of the provided txid
Return Information: Raw Transaction
Provides the txid of the raw transaction as an input.
The input has to be a string. 
"""

rawTxGetTool = Tool(
    name="get_raw_transaction",
    description=description,
    func=get
)
