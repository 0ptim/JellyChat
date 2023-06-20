from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_vaults(query: str) -> str:
    """Returns information about a vault."""
    requests = TextRequestsWrapper()
    return requests.get(f"https://ocean.defichain.com/v0/mainnet/loans/vaults/{query}")


description = """
Get information about one specific vault.
Provide the vault ID as input.
"""

vaultInformationTool = Tool(
    name="get_vault_information",
    description=description,
    func=get_vaults
)
