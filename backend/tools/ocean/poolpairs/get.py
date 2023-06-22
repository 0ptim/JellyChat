from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def get(query: str) -> [{}]:
    """Returns information to a specific pool pair"""
    return getOcean().poolpairs.get(query)


description = """
Gets a pool pair and the corresponding information.
Return Information: ID, Symbol, DisplaySymbol, Name, Status, tokenA: (Symbol, DisplaySymbol, ID, Name, Reserve, 
BlockCommission), tokenB: (Symbol, DisplaySymbol, ID, Name, Reserve, BlockCommission), PriceRatio: (ab, ba), Commission,
TotalLiquidity: (Token, USD), TradeEnabled, OwnerAddress, RewardPct, RewardLoanPct, Creation: (Tx, Height), 
APR: (Reward, Commission, Total), Volume: (h24, d30)
Provides the id of the pool pair as an input.
Only an ID is allowed as a identification for the pool pair. Use "List Pool Pairs" to get IDs.
The input has to be a string. 
"""

poolpairsGetTool = Tool(
    name="get_pool_pair",
    description=description,
    func=get
)
