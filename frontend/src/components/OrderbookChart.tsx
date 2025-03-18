import { useEffect, useRef, useState } from "react";
import { createChart, LineSeries } from "lightweight-charts";

interface OrderbookChartProps {
  LatestPrice: number | undefined;
}

const OrderbookChart = ({ LatestPrice }: OrderbookChartProps)  => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const [lineSeries, setLineSeries] = useState<any>(null);
  const lastTimestampRef = useRef<number | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current) {
      console.error("OrderbookChart: Chart container ref is null");
      return;
    }

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 300,
      layout: {
        background: { color: "#1F2937" },
        textColor: "#D1D5DB",
      },
      grid: {
        vertLines: { color: "#374151" },
        horzLines: { color: "#374151" },
      },
      rightPriceScale: { borderColor: "#4B5563"},
      timeScale: { borderColor: "#4B5563"},
    });

    try {
      const series = chart.addSeries(LineSeries, {
        color: "#10B981",
        lineWidth: 2,
      });
      series.setData([]);
      setLineSeries(series);
    } catch (error) {
      console.error("OrderbookChart: Error creating line series:", error);
    }

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
    };
  }, []);

  useEffect(() => {
    if (lineSeries && LatestPrice !== undefined) {
      let time = Math.floor(Date.now() / 1000);
      if (lastTimestampRef.current !== null && time <= lastTimestampRef.current) {
        time = lastTimestampRef.current + 1;
      }
      lastTimestampRef.current = time;
      try {
        lineSeries.update({ time, value: LatestPrice });
      } catch (error) {
        console.error("OrderbookChart: Error updating chart:", error);
      }
    }
  }, [LatestPrice, lineSeries]);

  return (
    <div className="w-full">
      <h2 className="text-xl font-semibold mb-2">Price Chart</h2>
      <div
        ref={chartContainerRef}
        className="bg-gray-800 rounded mb-8"
      />
      </div>
  );
};

export default OrderbookChart;