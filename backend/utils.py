from tools.wiki_qa import wikiTool
from tools.ocean.stats import statsTool
from tools.ocean.token_balance import tokenbalanceTool
from tools.ocean.transactions import transactionsTool
from tools.ocean.utxo_balance import utxoTool
from tools.ocean.vaults import vaultsForAddressTool
from tools.ocean.vault import vaultInformationTool


def get_tool_message(name: str) -> str:
    """depending on the tool name, return a message to the user"""
    if name == wikiTool.name:
        return "I'll go look this up in the DeFiChainWiki for you 🔎"
    elif name == statsTool.name:
        return "Let me gather the latest blockchain statistics for you 📊"
    elif name == tokenbalanceTool.name:
        return "Checking the token balance now ⚖️"
    elif name == transactionsTool.name:
        return "Fetching the transaction history 🔄"
    elif name == utxoTool.name:
        return "Let's check the UTXO balance 💱"
    elif name == vaultsForAddressTool.name:
        return "Analyzing vaults associated with the address 🏦"
    elif name == vaultInformationTool.name:
        return "Retrieving detailed vault information ℹ️"
    elif name == "Calculator":
        return "Let's do the math together 🧮"
    else:
        raise ValueError(f"Unknown tool name: {name}")
