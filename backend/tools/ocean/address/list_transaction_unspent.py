from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    address: str = Field(..., description="The address")


def list_transaction_unspent(address: str) -> str:
    return getOcean().address.listTransactionUnspent(address)


description = """List all unspent inputs belonging to an address"""

addressListTransactionUnspentTool = StructuredTool(
    name="list_unspent_inputs_of_address",
    description=description,
    func=list_transaction_unspent,
    args_schema=ToolInputSchema,
)
