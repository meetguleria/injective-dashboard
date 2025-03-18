import pandas as pd
import pandas_ta as ta
from typing import List, Dict, Any

class DataAggregator:
    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.data: List[Dict[str, Any]] = []  # Each entry is a dict with 'timestamp' and 'price'

    def add_update(self, update: Dict[str, Any]) -> None:
        try:
            orderbook = update.get("orderbook", {})
            buys = orderbook.get("buys", [])
            sells = orderbook.get("sells", [])

            if not buys or not sells:
                print("Update missing buys or sells")
                return

            # Calculate best bid (highest price) and best ask (lowest price)
            best_bid = max(float(bid["price"]) for bid in buys)
            best_ask = min(float(ask["price"]) for ask in sells)
            mid_price_raw = (best_bid + best_ask) / 2.0

            scale_factor = 1e12
            mid_price = mid_price_raw * scale_factor
            # Get timestamp from the update or use current time
            timestamp = update.get("timestamp")
            if timestamp is None:
                timestamp = pd.Timestamp.utcnow().timestamp() * 1000

            self.data.append({"timestamp": timestamp, "price": mid_price})
            print(f"Added mid_price: {mid_price}, total data points: {len(self.data)}")

            if len(self.data) > self.window_size:
                self.data.pop(0)
        except Exception as e:
            print(f"Error processing update: {e}")

    def compute_signals(self) -> Dict[str, Any]:
        if len(self.data) < self.window_size:
            print(f"Not enough data to compute signals: {len(self.data)}/{self.window_size}")
            return {}

        df = pd.DataFrame(self.data)
        df.sort_values("timestamp", inplace=True)
        
        df["RSI"] = ta.rsi(df["price"], length=14)
        macd_df = ta.macd(df["price"])
        df["MACD"] = macd_df["MACD_12_26_9"]
        df["MACD_signal"] = macd_df["MACDs_12_26_9"]
        df["SMA"] = ta.sma(df["price"], length=20)
        
        latest = df.iloc[-1]
        signals = {
            "LatestPrice": latest["price"],
            "RSI": latest["RSI"],
            "MACD": latest["MACD"],
            "MACD_signal": latest["MACD_signal"],
            "SMA": latest["SMA"]
        }
        print("Computed signals:", signals)
        return signals
