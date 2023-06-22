from langchain.agents import Tool

from ..utils import getOcean, Network


def get_reward_distribution(query: str) -> str:
    """Get reward distribution of DeFi Blockchain"""
    return getOcean().stats.getRewardDistribution()


description = """
Gets reward distribution information.
Information: masternode: int, community: int, anchor: int, liquidity: int, loan: int, options: int, unallocated: int
"""

statsGetRewardDistributionTool = Tool(
    name="gets_reward_distribution",
    description=description,
    func=get_reward_distribution
)
