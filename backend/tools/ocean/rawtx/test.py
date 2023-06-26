from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    raw_tx: str = Field(..., description="Raw transaction (hex string)")


def test(raw_tx: str) -> str:
    try:
        getOcean().rawTx.test(raw_tx)
        return True
    except Exception as e:
        return e


description = """Tests if the provided raw transaction is accepted by the network"""

rawTxTestTool = StructuredTool(
    name="test_raw_transaction",
    description=description,
    func=test,
    args_schema=ToolInputSchema,
)
