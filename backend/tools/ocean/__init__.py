# Imports

oceanTools = []

# Address
from .address.get_balance import addressGetBalanceTool
from .address.list_token import addressListTokenTool
from .address.list_transaction import addressListTransactionsTool
from .address.list_vault import addressListVaultTool

oceanTools.extend([addressGetBalanceTool, addressListTokenTool, addressListTransactionsTool, addressListVaultTool])

# Blocke
from .blocks.list import blocksListTool

oceanTools.extend([blocksListTool])

# Loan
from .loan.getVault import loanGetVaultTool

oceanTools.extend([loanGetVaultTool])

# PoolPairs
#from .poolpairs.get import poolpairsGetTool
#from .poolpairs.list import poolpairsListTool

#oceanTools.extend([poolpairsGetTool, poolpairsListTool])

# Prices
from .prices.get import priceGetTool

oceanTools.extend([priceGetTool])

# Stats
from .stats.get import statsGetTool
from .stats.getBurn import statsGetBurnTool
from .stats.getRewardDistribution import statsGetRewardDistributionTool
from .stats.getSupply import statsGetSupplyTool

oceanTools.extend([statsGetTool, statsGetBurnTool, statsGetRewardDistributionTool, statsGetSupplyTool])

# Tokens
from .tokens.get import tokenGetTool

oceanTools.extend((tokenGetTool, ))

# Transaction
from .transactions.get import transactionGetTool
from .transactions.get_vins import transactionGetVinsTool
from .transactions.get_vouts import transactionGetVoutsTool

oceanTools.extend((transactionGetTool, transactionGetVinsTool, transactionGetVoutsTool))


