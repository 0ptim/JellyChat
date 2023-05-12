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
from .loan.get_vault import loanGetVaultTool

oceanTools.extend([loanGetVaultTool])

# PoolPairs
#from .poolpairs.get import poolpairsGetTool
#from .poolpairs.list import poolpairsListTool

#oceanTools.extend([poolpairsGetTool, poolpairsListTool])

# Stats
from .stats.get import statsGetTool
from .stats.getBurn import statsGetBurnTool
from .stats.getRewardDistribution import statsGetRewardDistributionTool
from .stats.getSupply import statsGetSupplyTool

oceanTools.extend([statsGetTool, statsGetBurnTool, statsGetRewardDistributionTool, statsGetSupplyTool])
