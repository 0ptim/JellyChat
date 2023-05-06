from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool

from . import getOcean, Network


def get_stats(query: str) -> str:
    """Gets general stats about the blockchain."""
    return getOcean().stats.get()


description = """
Gets general real-time stats about the blockchain.
Block count, Burned coins, TVL, DFI Price, Masternode-Count, Difficulty etc.
"""

statsTool = Tool(
    name="Get Stats",
    description=description,
    func=get_stats
)
