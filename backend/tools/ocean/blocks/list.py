from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def list(query: str) -> str:
    """Returns a list of blocks"""
    return getOcean().blocks.list(query)


description = """
Lists the latest blocks with the corresponding information.
Return Information: ID, Hash, PreviousHash, Height, Version, Time, MedianTime, TransactionCount, Difficulty, Masternode, 
Minter, MinterBlockCount, StakeModifier, MerkleRoot, Size, SizeStripped, Weight, Reward
Provides the number of blocks as an input. Default input is 3.
The input has to be a string. 
"""

blocksListTool = Tool(
    name="List Latest Blocks",
    description=description,
    func=list
)
