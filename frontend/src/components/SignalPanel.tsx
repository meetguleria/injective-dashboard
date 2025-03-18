interface SignalPanelProps {
  signals: any;
}

const SignalPanel = ({ signals }: SignalPanelProps) => {
  if (!signals || Object.keys(signals).length === 0) {
    return (
      <div className="p-4 bg-gray-800 rounded">
        <p>Loading Signals...</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-gray-800 rounded">
      <h2 className="text-xl font-semibold mb-4">Computed Signals</h2>
      <ul className="space-y-2">
        <li>
          <strong>Latest Price:</strong> {signals.LatestPrice}
        </li>
        <li>
          <strong>RSI:</strong> {signals.RSI}
        </li>
        <li>
          <strong>MACD:</strong> {signals.MACD}
        </li>
        <li>
          <strong>MACD Signal:</strong> {signals.MACD_signal}
        </li>
        <li>
          <strong>SMA:</strong> {signals.SMA}
        </li>
      </ul>
    </div>
  );
};

export default SignalPanel;