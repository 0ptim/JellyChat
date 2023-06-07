from langchain.agents import Tool

from ..utils import getOcean, Network


def get_burn(query: str) -> str:
    """Get burn info of DeFi Blockchain"""
    return getOcean().stats.getBurn()


description = """
Gets burn information.
Information: address: str, amount: str, tokens: str[], feeburn: float, emissionburn: float, auctionburn: float, 
paybackburn: float, paybackburntokens: str[], dexfeetokens: str[], dfipaybackfee: float, dfipaybacktokens: str[], 
paybackfees: str[], paybacktokens: str[], dfip2203: str[], dfip2206f: str[]
"""

statsGetBurnTool = Tool(
    name="Gets Burn Information",
    description=description,
    func=get_burn
)
