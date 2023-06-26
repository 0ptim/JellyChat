from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from ..utils import getOcean


class ToolInputSchema(BaseModel):
    masternode_id: str = Field(..., description="The masternode ID")


def get(masternode_id: str) -> str:
    return getOcean().masternodes.get(masternode_id)


description = """Gets information about a masternode with given id"""

masternodeGetTool = StructuredTool(
    name="get_masternode",
    description=description,
    func=get,
    args_schema=ToolInputSchema,
)
