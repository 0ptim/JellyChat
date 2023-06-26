from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    txid: str = Field(..., description="The transaction ID")


def get(txid: str) -> str:
    return getOcean().rawTx.get(txid)


description = """Returns the raw transaction of the provided txid."""

rawTxGetTool = StructuredTool(
    name="get_raw_transaction",
    description=description,
    func=get,
    args_schema=ToolInputSchema,
)
