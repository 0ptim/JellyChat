from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    txid: str = Field(..., description="The id of the transaction")


def get_vouts(query: str) -> str:
    return getOcean().transactions.getVouts(query, size=200)


description = """Gets a list of outputs of a transaction with specified txid"""

transactionGetVoutsTool = StructuredTool(
    name="get_outputs_of_transaction",
    description=description,
    func=get_vouts,
    args_schema=ToolInputSchema,
)
