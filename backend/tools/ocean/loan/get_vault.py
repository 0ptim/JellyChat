from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool

from ..utils import getOcean, Network


def get_vault(query: str) -> str:
    """Returns information about a vault."""
    return getOcean().loan.getVault(query)


description = """
Get information about a vault with given vault id
Return Information: (vaultId: str, loanScheme: (id: str, minColRatio: int, interestRate: int), ownerAddress: str, state: str, 
informativeRatio: float, collateralRatio: int, collateralValue: float, loanValue: float, interestValue: float, 
collateralAmounts: [(id: int, amount: float, symbol: str, symbolKey: str, name: str, displaySymbol: str, 
activePrice: (id: str, key: str, isLive: bool, block: (hash: str, height: int, medianTime: int, time: int), 
active: (amount: float, weightage: int, oracles: (active: int, total: int)), next: (amount: float, weightage: int, 
oracles: (active: int, total: int)), sort: str))))
Provide the vault ID as input.
"""

loanGetVaultTool = Tool(
    name="get_vault_information",
    description=description,
    func=get_vault
)
