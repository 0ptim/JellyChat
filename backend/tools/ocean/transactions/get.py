from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    txid: str = Field(..., description="The id of the transaction")


def get(txid: str) -> str:
    return getOcean().transactions.get(txid)


description = """Get information about the transaction of the specified txid."""

transactionGetTool = StructuredTool(
    name="get_transaction",
    description=description,
    func=get,
    args_schema=ToolInputSchema,
)
