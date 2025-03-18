import { useState, useEffect } from 'react';

interface Market {
  market_id: string;
  symbol: string;
  base_asset?: string;
  quote_asset?: string;
}

interface MarketSelectorProps {
  onMarketChange: (marketSymbol: string) => void;
}

const MarketSelector = ({ onMarketChange }: MarketSelectorProps) => {
  const [markets, setMarkets] = useState<Market[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchMarkets = async () => {
      try {
        const response = await fetch('http://localhost:8000/markets?limit=20');
        if (!response.ok) {
          throw new Error('Failed to fetch markets');
        }
        const data: Market[] = await response.json();
        setMarkets(data);
      } catch (error) {
        console.error('Error fetching markets:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchMarkets();
  }, []);

  return (
    <div className='mb-4'>
      <label htmlFor="market-selector" className='mr-2'> Select Market: </label>
      {loading ? (
        <span>Loading Markets...</span>
      ) : (
        <select
          id="market-selector"
          onChange={(e) => onMarketChange(e.target.value)}
          className="p-2 rounded border"
          size={5}
          >
            {markets.map((market) => (
              <option key={market.market_id} value={market.symbol}>
                {market.symbol.toUpperCase()} ({market.base_asset}/{market.quote_asset})
              </option>
            ))}
          </select>
      )}
    </div>
  );
};

export default MarketSelector;