from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    address: str = Field(..., description="The address")
    limit: int = Field(..., description="Number of transactions to list")


def list_transaction(address: str, limit: int) -> str:
    return getOcean().address.listTransaction(address=address, size=limit)


description = """Lists transactions belonging to the specified address"""

addressListTransactionsTool = StructuredTool(
    name="get_address_transactions",
    description=description,
    func=list_transaction,
    args_schema=ToolInputSchema,
)
