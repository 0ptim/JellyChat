# Imports
from .address import *
from .blocks import *
from .governance import *
from .loan import *
from .masternodes import *
from .poolpairs import *
from .prices import *
from .rawtx import *
from .stats import *
from .tokens import *
from .transactions import *

oceanTools = []

# Address
oceanTools.extend((addressGetBalanceTool, addressListTokenTool, addressListTransactionsTool, addressListVaultTool,
                   addressListTransactionUnspentTool))

# Blocks
oceanTools.extend((blocksGetTool, blocksGetTransactionsTool, blocksListTool))

# Governance
oceanTools.extend((governanceGetGovProposalTool, governanceListGovProposalTool))

# Loan
oceanTools.extend((loanGetVaultTool, ))

# Masternode
oceanTools.extend((masternodeGetTool, ))

# PoolPairs
oceanTools.extend((poolpairsGetTool, ))

# Prices
oceanTools.extend((priceGetTool, ))

# RawTX
oceanTools.extend((rawTxGetTool, rawTxSendTool, rawTxTestTool))

# Stats
oceanTools.extend((statsGetTool, statsGetBurnTool, statsGetRewardDistributionTool, statsGetSupplyTool))

# Tokens
oceanTools.extend((tokenGetTool, ))

# Transaction
oceanTools.extend((transactionGetTool, transactionGetVinsTool, transactionGetVoutsTool))


