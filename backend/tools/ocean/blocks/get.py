from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def get(query: str) -> str:
    """Returns the specified block"""
    return getOcean().blocks.get(query)


description = """
Returns the corresponding information of the specified block.
Return Information: id: str, hash: str, previousHash: str, height: int, version: int, time: int, medianTime: int, 
transactionCount: int, difficulty: float, masternode: str, minter: str, minterBlockCount: int, reward: str, 
stakeModifier: str, merkleroot: str, size: int, sizeStripped: int, weight: int
Only an blockhash is allowed as a identification of the block.
The input has to be a string. 
"""

blocksGetTool = Tool(
    name="get_block",
    description=description,
    func=get
)
