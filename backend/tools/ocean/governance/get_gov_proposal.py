from langchain.agents import Tool

from ..utils import getOcean, Network, filterJson


def get_gov_proposal(query: str) -> str:
    """Get information about a proposal with given proposal id."""
    return getOcean().governance.getGovProposal(query)


description = """
Gets information about a proposal with given proposal id.
Return Information: 

proposalId: string
title: string
context: string
contextHash: string
type: GovernanceProposalType
status: GovernanceProposalStatus
amount?: string
currentCycle: number
totalCycles: number
creationHeight: number
cycleEndHeight: number
proposalEndHeight: number
payoutAddress?: string
votingPeriod: number
approvalThreshold: string
quorum: string
votesPossible?: number
votesPresent?: number
votesPresentPct?: string
votesYes?: number
votesYesPct?: string
fee: number
options?: string[]

Only an txid is allowed as a identification of the proposal.
The input has to be a string. 
"""

governanceGetGovProposalTool = Tool(
    name="Get Governance Proposal",
    description=description,
    func=get_gov_proposal
)
