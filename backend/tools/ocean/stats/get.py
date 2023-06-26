from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    placeholder: str = Field(..., description="Just fill in `asdf`")


def get(placeholder: str) -> str:
    return getOcean().stats.get()


description = """Gets general stats of DeFi Blockchain."""

statsGetTool = StructuredTool(
    name="get_stats",
    description=description,
    func=get,
    args_schema=ToolInputSchema,
)
