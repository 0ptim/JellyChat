from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_stats(query: str) -> str:
    """Gets general stats about the blockchain."""
    requests = TextRequestsWrapper()
    return requests.get("https://ocean.defichain.com/v0/mainnet/stats")


description = """
Gets general real-time stats about the blockchain.
Block count, Burned coins, TVL, DFI Price, Masternode-Count, Difficulty etc.
Pass in `asdf` to get the stats.
"""

statsTool = Tool(
    name="get_stats",
    description=description,
    func=get_stats
)
