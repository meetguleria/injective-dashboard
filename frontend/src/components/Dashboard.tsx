import { useState, useEffect } from 'react';
import OrderbookChart from './OrderbookChart';
import SignalPanel from './SignalPanel';
import MarketSelector from './MarketSelector';

export const Dashboard = () => {
  const [signals, setSignals] = useState<any>({});
  const [selectedMarket, setSelectedMarket] = useState<string>("inj/usdt");
  const [socket, setSocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    const wsUrl = `ws://localhost:8000/orderbook/${selectedMarket}/ws`;
    const newSocket = new WebSocket(wsUrl);
    setSocket(newSocket);

    newSocket.onopen = (event) => console.log("Dashboard: WebSocket connection opened:", event);
    newSocket.onmessage = (event) => {
      console.log("Dashboard: Received message:", event.data);
      try {
        const data = JSON.parse(event.data);
        if (data && data.LatestPrice) {
          setSignals(data);
        } else {
          console.warn("Dashboard: Incomplete data:", data);
        }
      } catch (error) {
        console.error("Dashboard: Error parsing message:", error);
      }
    };
    newSocket.onerror = (error) => console.error("Dashboard: WebSocket error:", error);
    newSocket.onclose = (event) => console.log("Dashboard: WebSocket connection closed:", event);

    return () => {
      console.log("Dashboard: Closing WebSocket connection.");
      newSocket.close();
    };
  }, [selectedMarket]);

  return (
    <div className='p-4'>
      <h1 className="text-3xl font-bold mb-6">Orderbook Signals</h1>
      <MarketSelector onMarketChange={(market) => setSelectedMarket(market)} />
      <div className="flex flex-col bg-red-500 p-4">
        <OrderbookChart LatestPrice={signals.LatestPrice} />
        <SignalPanel signals={signals} />
      </div>
    </div>
  );
};

export default Dashboard;