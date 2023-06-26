from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    placeholder: str = Field(..., description="Just fill in `asdf`")


def list_gov_proposal(placeholder: str) -> str:
    # Query Proposals
    proposals = []
    data = getOcean().governance.listGovProposals("all", "all", 0, True, size=200)
    proposals.extend(data.get("data"))

    next = data.get("page").get("next") if data.get("page") else None
    while next:
        data = getOcean().governance.listGovProposals(
            "all", "all", 0, True, size=200, next=next
        )
        proposals.extend(data.get("data"))
        next = data.get("page").get("next") if data.get("page") else None

    # Filter for Proposal ID and Title
    filtered_proposals = []
    for proposal in proposals:
        filtered_proposals.append(
            {"id": proposal.get("proposalId"), "title": proposal.get("title")}
        )
    return filtered_proposals


description = """Lists id and title of all proposals."""

governanceListGovProposalTool = StructuredTool(
    name="list_all_governance_proposal_ID_and_title",
    description=description,
    func=list_gov_proposal,
    args_schema=ToolInputSchema,
)
