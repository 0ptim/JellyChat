from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_vaults(query: str) -> str:
    """Returns the vaults of an address."""
    requests = TextRequestsWrapper()
    return requests.get(f"https://ocean.defichain.com/v0/mainnet/address/{query}/vaults")


description = """
To get the vaults of one specific address.
Provide the address as input. Example: df1...
"""

vaultsForAddressTool = Tool(
    name="Get Vaults for Address",
    description=description,
    func=get_vaults
)
