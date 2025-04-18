import asyncio
from pyinjective.async_client import AsyncClient
from pyinjective.core.network import Network
from services.data_aggregator import DataAggregator

# Create a global data aggregator instance
aggregator = DataAggregator(window_size=50)  # Use a smaller window for quicker signal generation

async def stream_orderbook(market_id: str, network: str = "mainnet"):
    network_obj = Network.mainnet() if network == "mainnet" else Network.testnet()
    client = AsyncClient(network_obj)
    queue = asyncio.Queue()
    
    def callback(event):
        #print("Callback triggered with event:", event)  # This will log raw updates in uvicorn logs
        asyncio.create_task(queue.put(event))
    
    def on_status_callback(exception):
        print(f"Error streaming order book for market {market_id}: {exception}")
    
    def on_end_callback():
        print("Stream ended for market", market_id)
    
    asyncio.create_task(
        client.listen_spot_orderbook_snapshots(
            market_ids=[market_id],
            callback=callback,
            on_end_callback=on_end_callback,
            on_status_callback=on_status_callback,
        )
    )
    
    while True:
        event = await queue.get()
        #print(f"Received orderbook update for {market_id}: {event}")  # Logs raw update
        aggregator.add_update(event)
        signals = aggregator.compute_signals()
        if signals:
            print("Computed Signals:", signals)  # Logs signals in uvicorn logs
            # Yield only the computed signals so that the WS client sees them
            yield signals
