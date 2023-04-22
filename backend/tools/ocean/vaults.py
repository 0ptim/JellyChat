from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_vaults(query: str) -> str:
    """Returns the vaults of an address."""
    requests = TextRequestsWrapper()
    return requests.get(f"https://ocean.defichain.com/v0/mainnet/address/{query}/vaults")


vaultsTool = Tool(
    name="Get Vaults",
    description="To get the vaults of one specific address.",
    func=get_vaults
)
