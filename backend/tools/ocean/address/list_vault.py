from langchain.agents import Tool

from ..utils import getOcean, Network


def list_vault(query: str) -> str:
    """Returns the vaults of an address."""
    return getOcean().address.listVault(query)


description = """
Lists vaults belonging to the specified address
Return information: vaultId: string, loanScheme: LoanScheme, ownerAddress: string, 
state: LoanVaultState.ACTIVE | LoanVaultState.FROZEN | LoanVaultState.MAY_LIQUIDATE | LoanVaultState.UNKNOWN,
informativeRatio: string, collateralRatio: string, collateralValue: string, loanValue: string, interestValue: string,
collateralAmounts: (id: string, amount: string, symbol: string, displaySymbol: string,symbolKey: string,name: string, 
activePrice?: ActivePrice), loanAmounts: (id: string, amount: string, symbol: string, displaySymbol: string, 
symbolKey: string,name: string, activePrice?: ActivePrice), interestAmounts: (id: string, amount: string,symbol: string,
displaySymbol: string, symbolKey: string, name: string, activePrice?: ActivePrice)
Provides a address as an input.
The input has to ba a string.
"""

addressListVaultTool = Tool(
    name="get_vaults_of_address",
    description=description,
    func=list_vault
)
