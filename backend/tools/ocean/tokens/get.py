from langchain.agents import Tool

from ..utils import getOcean, Network


def get(query: str) -> str:
    """Get information about a token with id of the token"""
    return getOcean().tokens.get(query)


description = """
Get information about a token with id of the token
Information: id: str, symbol: str, displaySymbol: str, symbolKey: str, name: str, decimal: float, limit: str, 
mintable: bool, tradeable: bool, isDAT: bool, isLPS: bool, isLoanToken: bool, finalized: bool, minted: str, 
creation: (tx: str, height: int), destruction: (tx: str, height: int), collateralAddress: str
Provides the id of the token as an input.
Only an ID is allowed as a identification for the token. Use "List Tokens" Tool to get IDs.
The input has to be a string. 
"""

tokenGetTool = Tool(
    name="Get Tokens",
    description=description,
    func=get
)
