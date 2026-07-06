"use client";

import { useEffect, useState } from "react";

const MARKET_ASSETS = {
  Stocks: [
    { label: "Tesla", ticker: "TSLA" },
    { label: "Nvidia", ticker: "NVDA" },
    { label: "Apple", ticker: "AAPL" },
    { label: "Microsoft", ticker: "MSFT" },
    { label: "Amazon", ticker: "AMZN" },
    { label: "Meta", ticker: "META" },
    { label: "Google", ticker: "GOOGL" },
  ],
  Crypto: [
    { label: "Bitcoin", ticker: "BTC" },
    { label: "Ethereum", ticker: "ETH" },
    { label: "Solana", ticker: "SOL" },
    { label: "Dogecoin", ticker: "DOGE" },
  ],
  Commodities: [
    { label: "Gold", ticker: "GOLD" },
    { label: "Silver", ticker: "SILVER" },
    { label: "Oil", ticker: "OIL" },
    { label: "Natural Gas", ticker: "NATGAS" },
    { label: "Copper", ticker: "COPPER" },
  ],
};

export default function Home() {
  const [ticker, setTicker] = useState("TSLA");
  const [assetClass, setAssetClass] = useState("Stocks");
  const [selectedAsset, setSelectedAsset] = useState("TSLA");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedSource, setSelectedSource] = useState("All");

  const fetchLiveScore = async () => {
    try {
      setLoading(true);

      const backendHost =
        window.location.hostname === "localhost" ||
        window.location.hostname === "127.0.0.1"
          ? "127.0.0.1"
          : window.location.hostname;

      const response = await fetch(`http://${backendHost}:8000/analyze/${ticker}`);
      const result = await response.json();

      setData(result);
      setSelectedSource("All");
    } catch (error) {
      console.error("Live score fetch failed:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      fetchLiveScore();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const analyzeTicker = async () => {
    setLoading(true);
    setData(null);

    try {
      const backendHost =
          window.location.hostname === "localhost" ||
          window.location.hostname === "127.0.0.1"
            ? "127.0.0.1"
            : window.location.hostname;

        const response = await fetch(
          `http://${backendHost}:8000/analyze/${ticker}`
        );
      const result = await response.json();
      setData(result);
      setSelectedSource("All");
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  const getSignalColor = (signal) => {
    if (signal === "Bullish") return "text-emerald-400";
    if (signal === "Bearish") return "text-rose-400";
    return "text-slate-300";
  };

  const getBadgeStyle = (signal) => {
    if (signal === "Bullish") return "bg-emerald-500/10 text-emerald-300 border-emerald-500/40";
    if (signal === "Bearish") return "bg-rose-500/10 text-rose-300 border-rose-500/40";
    return "bg-slate-500/10 text-slate-300 border-slate-500/40";
  };

  const articles = data?.articles || [];

  const sources = [
    "All",
    ...Array.from(new Set(articles.map((item) => item.source_type))),
  ];

  const filteredArticles =
    selectedSource === "All"
      ? articles
      : articles.filter((item) => item.source_type === selectedSource);

  const getSourceCount = (source) => {
    if (source === "All") return articles.length;
    return articles.filter((item) => item.source_type === source).length;
  };

  return (
    <main className="min-h-screen bg-[#050816] text-white overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,#1f8bff33,transparent_35%),radial-gradient(circle_at_top_right,#22c55e22,transparent_30%),radial-gradient(circle_at_bottom,#9333ea22,transparent_35%)]" />

      <div className="relative z-10">
        <section className="px-8 pt-10 pb-8 border-b border-white/10">
          <div className="max-w-7xl mx-auto">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-slate-300 mb-6">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              Live multi-source market intelligence
            </div>

            <h1 className="text-5xl md:text-7xl font-black tracking-tight">
              Insider<span className="text-emerald-400">IQ</span>
            </h1>

            <p className="text-slate-300 mt-4 max-w-2xl text-lg">
              Track bullish and bearish momentum across news, Reddit, YouTube,
              crypto, stocks, and commodities using FinBERT-powered analysis.
            </p>
          </div>
        </section>

        <section className="max-w-7xl mx-auto px-8 py-8">
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-6 shadow-2xl mb-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <select
                value={assetClass}
                onChange={(e) => {
                  const newClass = e.target.value;
                  setAssetClass(newClass);
                  setSelectedAsset(MARKET_ASSETS[newClass][0].ticker);
                  setTicker(MARKET_ASSETS[newClass][0].ticker);
                }}
                className="bg-[#0b1020] border border-white/10 rounded-2xl px-4 py-3 outline-none focus:border-emerald-400"
              >
                {Object.keys(MARKET_ASSETS).map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>

              <select
                value={selectedAsset}
                onChange={(e) => {
                  setSelectedAsset(e.target.value);
                  setTicker(e.target.value);
                }}
                className="bg-[#0b1020] border border-white/10 rounded-2xl px-4 py-3 outline-none focus:border-emerald-400"
              >
                {MARKET_ASSETS[assetClass].map((asset) => (
                  <option key={asset.ticker} value={asset.ticker}>
                    {asset.label} ({asset.ticker})
                  </option>
                ))}
              </select>

              <input
                type="text"
                value={ticker}
                onChange={(e) => setTicker(e.target.value.toUpperCase())}
                placeholder="Custom ticker"
                className="bg-[#0b1020] border border-white/10 rounded-2xl px-4 py-3 outline-none focus:border-emerald-400"
              />

              <button
                onClick={fetchLiveScore}
                disabled={loading}
                className="px-6 py-3 rounded-2xl bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed text-black font-semibold transition-all duration-200 shadow-lg shadow-emerald-500/20"
              >
                {loading ? "Analyzing..." : "Analyze Ticker"}
              </button>

              <p className="text-sm text-gray-400">
                Last updated: {data?.last_updated || "Not updated yet"}
              </p>
              {loading && (
                <p className="mt-3 text-sm text-emerald-400">
                  Updating live score for {ticker}...
                </p>
              )}
            </div>
          </div>

          {data && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-5 mb-8">
                <div className="rounded-3xl bg-white/5 border border-white/10 p-6">
                  <p className="text-slate-400 text-sm">Asset</p>
                  <h2 className="text-4xl font-black mt-2">{data.ticker}</h2>
                </div>

                <div className="rounded-3xl bg-white/5 border border-white/10 p-6">
                  <p className="text-slate-400 text-sm">Overall Signal</p>
                  <h2 className={`text-4xl font-black mt-2 ${getSignalColor(data.overall_signal)}`}>
                    {data.overall_signal}
                  </h2>
                </div>

                <div className="rounded-3xl bg-white/5 border border-white/10 p-6">
                  <p>AI Score</p>
                  <h2>{data?.ai_score ?? "--"}/100</h2>
                  <p>{data?.confidence || "No confidence yet"} confidence</p>
                  <p>{data?.overall_signal || "No signal yet"}</p>
                  <p className="text-sm text-gray-400">
                    Last updated: {data?.last_updated || "Not updated yet"}
                  </p>
                  <h2 className="text-4xl font-black mt-2">{data.average_score}</h2>
                </div>

                <div className="rounded-3xl bg-white/5 border border-white/10 p-6">
                  <p className="text-slate-400 text-sm">Sources Found</p>
                  <h2 className="text-4xl font-black mt-2">{sources.length - 1}</h2>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
                <div className="rounded-3xl bg-emerald-500/10 border border-emerald-500/30 p-6">
                  <p className="text-emerald-300">Bullish Signals</p>
                  <h2 className="text-5xl font-black mt-2">{data.bullish_count}</h2>
                </div>

                <div className="rounded-3xl bg-rose-500/10 border border-rose-500/30 p-6">
                  <p className="text-rose-300">Bearish Signals</p>
                  <h2 className="text-5xl font-black mt-2">{data.bearish_count}</h2>
                </div>

                <div className="rounded-3xl bg-slate-500/10 border border-slate-500/30 p-6">
                  <p className="text-slate-300">Neutral Signals</p>
                  <h2 className="text-5xl font-black mt-2">{data.neutral_count}</h2>
                </div>
              </div>

              <div className="rounded-3xl bg-white/5 border border-white/10 p-5 mb-8">
                <h2 className="text-2xl font-bold mb-4">Source Command Center</h2>

                <div className="flex flex-wrap gap-3">
                  {sources.map((source) => (
                    <button
                      key={source}
                      onClick={() => setSelectedSource(source)}
                      className={`px-4 py-2 rounded-full border transition ${
                        selectedSource === source
                          ? "bg-emerald-500 text-black border-emerald-400 font-bold"
                          : "bg-white/5 border-white/10 text-slate-300 hover:border-emerald-400/50"
                      }`}
                    >
                      {source} ({getSourceCount(source)})
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <h2 className="text-3xl font-black mb-6">Intelligence Feed</h2>

                <div className="space-y-5">
                  {filteredArticles.map((article, index) => (
                    <div
                      key={index}
                      className={`group rounded-3xl bg-white/5 border p-6 hover:bg-white/[0.07] transition ${
                        article.source_type === "SEC Filing"
                          ? "border-amber-500/40 hover:border-amber-400/70"
                          : "border-white/10 hover:border-emerald-400/40"
                      }`}
                    >
                      <div className="flex flex-col md:flex-row justify-between gap-6">
                        <div className="flex-1">
                          <div className="flex flex-wrap gap-3 mb-4">
                            <span className="px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 text-sm">
                              {article.source_type}
                            </span>

                            <span className={`px-3 py-1 rounded-full border text-sm ${getBadgeStyle(article.sentiment)}`}>
                              {article.sentiment}
                            </span>
                          </div>

                          <h3 className="text-xl md:text-2xl font-bold mb-3 group-hover:text-emerald-300 transition">
                            {article.title}
                          </h3>

                          <p className="text-slate-400 mb-4">{article.publisher}</p>
                            {article.source_type === "SEC Filing" && (
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
                                <div className="rounded-2xl bg-amber-500/10 border border-amber-500/30 p-3">
                                  <p className="text-amber-300 text-xs uppercase tracking-wide">
                                    Filing Type
                                  </p>
                                  <p className="font-bold text-white">{article.filing_type}</p>
                                </div>

                                <div className="rounded-2xl bg-amber-500/10 border border-amber-500/30 p-3">
                                  <p className="text-amber-300 text-xs uppercase tracking-wide">
                                    Event Type
                                  </p>
                                  <p className="font-bold text-white">{article.event_type}</p>
                                </div>

                                <div className="rounded-2xl bg-amber-500/10 border border-amber-500/30 p-3">
                                  <p className="text-amber-300 text-xs uppercase tracking-wide">
                                    Importance
                                  </p>
                                  <p className="font-bold text-white">{article.importance}</p>
                                </div>
                              </div>
                            )}
                          <a
                            href={article.link}
                            target="_blank"
                            rel="noreferrer"
                            className="text-emerald-400 hover:text-emerald-300 font-semibold"
                          >
                            Open Source →
                          </a>
                        </div>

                        {article.source_type === "SEC Filing" ? (
                          <div className="min-w-[220px]">
                            <div className="rounded-2xl bg-amber-500/10 border border-amber-500/30 p-4">
                              <p className="text-amber-300 text-xs uppercase tracking-wide mb-2">
                                SEC Event
                              </p>

                              <div className="space-y-3">
                                <div>
                                  <p className="text-slate-400 text-sm">Filing Date</p>
                                  <p className="font-bold text-white">
                                    {article.filing_date}
                                  </p>
                                </div>

                                <div>
                                  <p className="text-slate-400 text-sm">Importance</p>
                                  <p
                                    className={`font-bold ${
                                      article.importance === "High"
                                        ? "text-red-300"
                                        : "text-amber-300"
                                    }`}
                                  >
                                    {article.importance}
                                  </p>
                                </div>

                                <div>
                                  <p className="text-slate-400 text-sm">Event Type</p>
                                  <p className="font-bold text-white">
                                    {article.event_type}
                                  </p>
                                </div>
                              </div>
                            </div>
                          </div>
                        ) : (
                          <div className="grid grid-cols-3 md:block gap-4 md:text-right min-w-[180px]">
                            <div className="mb-3">
                              <p className="text-slate-500 text-sm">Raw</p>
                              <p className="text-xl font-black">{article.score}</p>
                            </div>

                            <div className="mb-3">
                              <p className="text-slate-500 text-sm">Weight</p>
                              <p className="text-xl font-black">
                                {article.source_weight}
                              </p>
                            </div>

                            <div>
                              <p className="text-slate-500 text-sm">Weighted</p>
                              <p className="text-xl font-black">
                                {article.weighted_score}
                              </p>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </section>
      </div>
    </main>
  );
}