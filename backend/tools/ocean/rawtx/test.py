from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def test(query: str) -> [{}]:
    """Test a raw transaction"""
    try:
        getOcean().rawTx.test(query)
        return True
    except Exception as e:
        return e


description = """
Tests if the provided raw transaction is accepted by the network
Return Information: bool
Provides a raw transaction (hex string) as an input.
The input has to be a string. 
"""

rawTxTestTool = Tool(
    name="test_raw_transaction",
    description=description,
    func=test
)
