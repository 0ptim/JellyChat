from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


from ..utils import getOcean


class ToolInputSchema(BaseModel):
    ticker_symbol: str = Field(..., description="The ticker symbol")


def get(ticker_symbol: str) -> str:
    return getOcean().prices.get(ticker_symbol, "USD")


description = """Gets a price ticker and the corresponding information."""

priceGetTool = StructuredTool(
    name="get_price_ticker",
    description=description,
    func=get,
    args_schema=ToolInputSchema,
)
