from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_vaults(query: str) -> str:
    """Returns the vaults of an address."""
    requests = TextRequestsWrapper()
    return requests.get(f"https://ocean.defichain.com/v0/mainnet/address/{query}/vaults")


description = """
To get the vaults of one specific address.
Provide the address as input. Example: df1qgq0rjw09hr6vr7sny2m55hkr5qgze5l9hcm0lg
"""

vaultsTool = Tool(
    name="Get Vaults",
    description=description,
    func=get_vaults
)
