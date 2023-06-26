from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    placeholder: str = Field(..., description="Just fill in `asdf`")


def get_burn(placeholder: str) -> str:
    return getOcean().stats.getBurn()


description = """Gets burn information."""

statsGetBurnTool = StructuredTool(
    name="gets_burn_information",
    description=description,
    func=get_burn,
    args_schema=ToolInputSchema,
)
