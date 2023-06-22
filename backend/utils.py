from tools.wiki_qa import wikiTool
from tools.ocean import oceanTools


def get_tool_message(name: str) -> str:
    """depending on the tool name, return a message to the user"""
    if name == wikiTool.name:
        return "I'll go look this up in the DeFiChainWiki for you 🔎"
    elif name in [tool.name for tool in oceanTools]:
        tool = " ".join([n.capitalize() for n in name.split("_")])
        return f"Let me gather some information out of the Ocean for you: {tool} 🌊"
    elif name == "Calculator":
        return "Let's do the math together 🧮"
    else:
        raise ValueError(f"Unknown tool name: {name}")
