from langchain.agents import Tool

from ..utils import getOcean, Network


def list_vault(query: str) -> str:
    """Returns the vaults of an address."""
    return getOcean().address.listVault(query)


description = """
To get the vaults of one specific address.
Provide the address as input. Example: df1...
"""

addressListVaultTool = Tool(
    name="Get Vaults for Address",
    description=description,
    func=list_vault
)
