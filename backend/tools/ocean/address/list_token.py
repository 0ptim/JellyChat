from langchain.agents import Tool

from ..utils import getOcean, Network


def list_token(query: str) -> str:
    """Returns the token balance of an address."""
    return getOcean().address.listToken(query)


description = """
Gets the balance of all tokens on a address.
Contains: DFI, BTC, ETH, USDC, USDT, DOGE, DUSD, SPY, TSLA, APPL, ...
Does not contain DFI UTXO balance.
Return information: id: str, amount: str, symbol: str, displaySymbol: str, symbolKey: str, name: str, isDAT: bool, 
isLPS: bool, isLoanToken: bool
Provides a address as an input.
The input has to be a string.
"""

addressListTokenTool = Tool(
    name="get_token_balance",
    description=description,
    func=list_token
)
