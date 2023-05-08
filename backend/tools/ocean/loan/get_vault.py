from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool

from ..utils import getOcean, Network


def get_vault(query: str) -> str:
    """Returns information about a vault."""
    return getOcean().loan.getVault(query)


description = """
Get information about one specific vault.
Provide the vault ID as input.
"""

loanGetVaultTool = Tool(
    name="Get Vault Information",
    description=description,
    func=get_vault
)
