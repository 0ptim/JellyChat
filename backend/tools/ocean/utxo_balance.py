from langchain.utilities import TextRequestsWrapper
from langchain.agents import Tool


def get_balance(query: str) -> str:
    """Returns the UTXO balance of an address."""
    requests = TextRequestsWrapper()
    return requests.get(f"https://ocean.defichain.com/v0/mainnet/address/{query}/balance")


description = """
To get the UTXO balance of one specific address.
Provide the address as input. Example: df1qgq0rjw09hr6vr7sny2m55hkr5qgze5l9hcm0lg
"""

balanceTool = Tool(
    name="Get UTXO Balance",
    description=description,
    func=get_balance
)
