from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_stats(query: str) -> str:
    """Gets general stats about the blockchain."""
    requests = TextRequestsWrapper()
    return requests.get("https://ocean.defichain.com/v0/mainnet/stats")


statsTool = Tool(
    name="Get Stats",
    description="Gets general real-time stats about the blockchain.",
    func=get_stats
)
