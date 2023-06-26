from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    poolpair_id: str = Field(..., description="The pool pair ID")


def get(poolpair_id: str) -> str:
    return getOcean().poolpairs.get(poolpair_id)


description = """Gets a pool pair and the corresponding information.
Use "List Pool Pairs" to get IDs."""

poolpairsGetTool = StructuredTool(
    name="get_pool_pair",
    description=description,
    func=get,
    args_schema=ToolInputSchema,
)
