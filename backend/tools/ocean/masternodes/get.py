from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def get(query: str) -> [{}]:
    """Get information about a masternode with given id"""
    return getOcean().masternodes.get(query)


description = """
Gets information about a masternode with given id
Return Information: id: str, sort: str, state: MasternodeState, mintedBlocks: int, owner: (address: str), 
operator: (address: str), creation: (height: int), resign: (tx: str, height: int), timelock: int
Provides the masternode id as an input.
The input has to be a string. 
"""

masternodeGetTool = Tool(
    name="Get Masternode",
    description=description,
    func=get
)
