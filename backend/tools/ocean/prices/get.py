from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def get(query: str) -> [{}]:
    """Returns a price ticker of a token"""
    return getOcean().prices.get(query, "USD")


description = """
Gets a price ticker and the corresponding information.
Information: id: str, sort: str, price: PriceFeed
Provides the name of the token as an input.
"""

priceGetTool = Tool(
    name="Get Price Ticker",
    description=description,
    func=get
)