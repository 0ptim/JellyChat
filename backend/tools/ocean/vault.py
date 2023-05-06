from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool

from . import getOcean, Network


def get_vaults(query: str) -> str:
    """Returns information about a vault."""
    return getOcean().loan.getVault(query)


description = """
Get information about one specific vault.
Provide the vault ID as input.
"""

vaultInformationTool = Tool(
    name="Get Vault Information",
    description=description,
    func=get_vaults
)
