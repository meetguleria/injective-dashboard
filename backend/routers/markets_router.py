import asyncio
from fastapi import APIRouter, HTTPException
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
from config import settings

router = APIRouter()

@router.get("")
async def get_markets(limit: int = 20, offset: int = 0, network: str = settings.network):
  try:
    network_obj = Network.mainnet() if network == 'mainnet' else Network.testnet()
    client = AsyncClient(network_obj)
    markets = await client.get_markets()
    markets_list = [
      {
        "market_id": market.market_id,
        "symbol": market.symbol,
        "base_symbol": market.base_symbol,
        "quote_symbol": market.quote_symbol,
      }
      for market in markets
    ]
    # Pagination
    paginated_markets = markets_list[offset:offset+limit]
    return paginated_markets
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error fetching markets: {e}")
  