from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def list_gov_proposal(query: str) -> []:
    """List just the proposal id and the title"""
    # Query Proposals
    proposals = []
    data = getOcean().governance.listGovProposals("all", "all", 0, True, size=200)
    proposals.extend(data.get("data"))

    next = data.get("page").get("next") if data.get("page") else None
    while next:
        data = getOcean().governance.listGovProposals("all", "all", 0, True, size=200, next=next)
        proposals.extend(data.get("data"))
        next = data.get("page").get("next") if data.get("page") else None

    # Filter for Proposal ID and Title
    filtered_proposals = []
    for proposal in proposals:
        filtered_proposals.append({"id": proposal.get("proposalId"), "title": proposal.get("title")})
    return filtered_proposals


description = """
Lists id and title of all proposals.

Return Information: 
proposalId: string
title: string
"""

governanceListGovProposalTool = Tool(
    name="List all Governance Proposal ID and Title",
    description=description,
    func=list_gov_proposal
)
