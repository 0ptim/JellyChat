from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool

from . import getOcean, Network


def get_vaults(query: str) -> str:
    """Returns the vaults of an address."""
    return getOcean().address.listVault(query)


description = """
To get the vaults of one specific address.
Provide the address as input. Example: df1...
"""

vaultsForAddressTool = Tool(
    name="Get Vaults for Address",
    description=description,
    func=get_vaults
)
