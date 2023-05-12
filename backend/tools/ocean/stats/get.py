from langchain.agents import Tool

from ..utils import getOcean, Network


def get(query: str) -> str:
    """Get stats of DeFi Blockchain"""
    return getOcean().stats.get()


description = """
Gets general stats of DeFi Blockchain
Information: count: (blocks: int, tokens: int, prices: int, masternodes: int), tvl: (total: float, dex: float, 
loan: float, masternodes: float), burned: (total: float, address: float, fee: int, auction: float, payback: float, 
emission: float), price: (usd: float, usdt: float), masternodes: (locked: [( weeks: int, tvl: float, count: int)]), 
emission: (total: float, masternode: float, dex: float, community: float, anchor: float, burned: float), 
loan: (count: (schemes: int, loanTokens: int, collateralTokens: int, openVaults: int, openAuctions: int), 
value: (collateral: float, loan: float)), blockchain: (difficulty: float), net: (version: int, subversion: str, 
protocolversion: int)
"""

statsGetTool = Tool(
    name="Get Stats",
    description=description,
    func=get
)
