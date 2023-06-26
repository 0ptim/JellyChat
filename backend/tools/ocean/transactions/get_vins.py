from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    txid: str = Field(..., description="The id of the transaction")


def get_vins(txid: str) -> str:
    return getOcean().transactions.getVins(txid, size=200)


description = """Gets a list of inputs of a transaction with specified txid"""

transactionGetVinsTool = StructuredTool(
    name="get_inputs_of_transaction",
    description=description,
    func=get_vins,
    args_schema=ToolInputSchema,
)
