def get_tool_message(name: str) -> str:
    """depending on the tool name, return a message to the user"""
    if name == "DeFiChainWiki QA System":
        return "I'll go look this up in the DeFiChainWiki for you 🔎"
    elif name == "Get Stats":
        return "Let me gather the latest blockchain statistics for you 📊"
    elif name == "Get Token Balance":
        return "Checking the token balance now ⚖️"
    elif name == "Get Transactions":
        return "Fetching the transaction history 🔄"
    elif name == "Get UTXO Balance":
        return "Let's check the UTXO balance 💱"
    elif name == "Get Vaults for Address":
        return "Analyzing vaults associated with the address 🏦"
    elif name == "Get Vault Information":
        return "Retrieving detailed vault information ℹ️"
    elif name == "Calculator":
        return "Let's do the math together 🧮"
    else:
        raise ValueError(f"Unknown tool name: {name}")
