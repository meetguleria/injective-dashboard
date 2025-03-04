import pandas as pd
import pandas_ta as ta
from typing import List, Dict, Any

class DataAggregator:
    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.data: List[Dict[str, Any]] = []  # List of dicts with keys: 'timestamp' and 'price'
    
    def add_update(self, update: Dict[str, Any]) -> None:
        """
        Processes an orderbook update. It extracts the best bid and best ask from the update
        and calculates the mid-price. Then, it adds the data to the sliding window.
        """
        try:
            orderbook = update.get("orderbook", {})
            buys = orderbook.get("buys", [])
            sells = orderbook.get("sells", [])
            
            # Ensure we have both bid and ask data
            if not buys or not sells:
                return
            
            # Best bid: highest price among buys
            best_bid = max(float(bid["price"]) for bid in buys)
            # Best ask: lowest price among sells
            best_ask = min(float(ask["price"]) for ask in sells)
            
            mid_price = (best_bid + best_ask) / 2.0
            
            # Use provided timestamp or current time (in milliseconds)
            timestamp = update.get("timestamp")
            if timestamp is None:
                timestamp = pd.Timestamp.utcnow().timestamp() * 1000
            
            # Add to our data list
            self.data.append({"timestamp": timestamp, "price": mid_price})
            
            # Maintain sliding window size
            if len(self.data) > self.window_size:
                self.data.pop(0)
        except Exception as e:
            print(f"Error processing update: {e}")
    
    def compute_signals(self) -> Dict[str, Any]:
        """
        Computes technical indicators using the current sliding window of prices.
        Returns a dictionary with signals.
        """
        # Require enough data
        if len(self.data) < self.window_size:
            return {}
        
        df = pd.DataFrame(self.data)
        # Sort by timestamp to ensure correct order
        df.sort_values("timestamp", inplace=True)
        
        # Compute RSI (e.g., with a 14-period)
        df["RSI"] = ta.rsi(df["price"], length=14)
        # Compute MACD (default parameters: fast=12, slow=26, signal=9)
        macd_df = ta.macd(df["price"])
        df["MACD"] = macd_df["MACD_12_26_9"]
        df["MACD_signal"] = macd_df["MACDs_12_26_9"]
        # Compute a 20-period Simple Moving Average (SMA)
        df["SMA"] = ta.sma(df["price"], length=20)
        
        # Take the latest computed values as our signals
        latest = df.iloc[-1]
        signals = {
            "LatestPrice": latest["price"],
            "RSI": latest["RSI"],
            "MACD": latest["MACD"],
            "MACD_signal": latest["MACD_signal"],
            "SMA": latest["SMA"]
        }
        return signals
