from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    height_or_hash: str = Field(..., description="The height or hash")


def get(height_or_hash: str) -> str:
    return getOcean().blocks.get(height_or_hash)


description = """Returns the corresponding information of the specified block."""

blocksGetTool = StructuredTool(
    name="get_block",
    description=description,
    func=get,
    args_schema=ToolInputSchema,
)
