from langchain.agents import Tool

from ..utils import getOcean, Network


def getSupply(query: str) -> str:
    """Gets supply of DeFi Blockchain"""
    return getOcean().stats.getSupply()


description = """
Gets supply information.
Information: max: float, total: float, burned: float, circulating: float
"""

statsGetSupplyTool = Tool(
    name="Gets Supply",
    description=description,
    func=getSupply
)