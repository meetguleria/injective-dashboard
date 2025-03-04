from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from config import settings
from streams.orderbook import stream_orderbook
import asyncio

router = APIRouter()

@router.websocket("/{market_id}/ws")
async def orderbook_ws(websocket: WebSocket, market_id: str):
  await websocket.accept()
  try:
    # Stream orderbook updates from the pyinjective SDK
    async for update in stream_orderbook(market_id):
      await websocket.send_json(update)
  except WebSocketDisconnect:
    print(f"Client disconnected from {market_id}")
  except Exception as e:
    print(f"Error streaming order book: {e}")
    await websocket.close()
