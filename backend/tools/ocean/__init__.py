from .address import (
    addressGetBalanceTool,
    addressListTokenTool,
    addressListTransactionsTool,
    addressListVaultTool,
    addressListTransactionUnspentTool,
)
from .blocks import (
    blocksGetTool,
    blocksGetTransactionsTool,
    blocksListTool,
)
from .governance import (
    governanceGetGovProposalTool,
    governanceListGovProposalTool,
)
from .loan import loanGetVaultTool
from .masternodes import masternodeGetTool
from .poolpairs import poolpairsGetTool
from .prices import priceGetTool
from .rawtx import (
    rawTxGetTool,
    rawTxSendTool,
    rawTxTestTool,
)
from .stats import (
    statsGetTool,
    statsGetBurnTool,
    statsGetRewardDistributionTool,
    statsGetSupplyTool,
)
from .tokens import tokenGetTool
from .transactions import (
    transactionGetVinsTool,
    transactionGetVoutsTool,
)

oceanTools = []

# Address
oceanTools.extend(
    (
        addressGetBalanceTool,
        addressListTokenTool,
        addressListTransactionsTool,
        addressListVaultTool,
        addressListTransactionUnspentTool,
    )
)

# Blocks
oceanTools.extend((blocksGetTool, blocksGetTransactionsTool, blocksListTool))

# Governance
oceanTools.extend((governanceGetGovProposalTool, governanceListGovProposalTool))

# Loan
oceanTools.extend((loanGetVaultTool,))

# Masternode
oceanTools.extend((masternodeGetTool,))

# PoolPairs
oceanTools.extend((poolpairsGetTool,))

# Prices
oceanTools.extend((priceGetTool,))

# RawTX
oceanTools.extend((rawTxGetTool, rawTxSendTool, rawTxTestTool))

# Stats
oceanTools.extend(
    (statsGetTool, statsGetBurnTool, statsGetRewardDistributionTool, statsGetSupplyTool)
)

# Tokens
oceanTools.extend((tokenGetTool,))

# Transaction
oceanTools.extend((transactionGetVinsTool, transactionGetVoutsTool))
