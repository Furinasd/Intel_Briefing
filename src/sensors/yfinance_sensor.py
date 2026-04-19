import yfinance as yf
from loguru import logger
from typing import Dict, Any, List

class YFinanceSensor:
    def __init__(self, tickers: List[str] = None):
        # Default target tickers: Core tech and market indicators.
        self.tickers = tickers or ["QQQ", "SPY", "NVDA", "AAPL", "MSFT", "TSLA", "^VIX"]

    def fetch_market_data(self) -> Dict[str, Any]:
        """Fetches current market data for configured tickers."""
        logger.info(f"Fetching yfinance data for {self.tickers}")
        market_stats = {}
        for ticker in self.tickers:
            try:
                t = yf.Ticker(ticker)
                # history(period="1d") returns latest trading day data
                hist = t.history(period="1d")
                if hist.empty:
                    logger.warning(f"No pricing data found for {ticker}")
                    continue
                
                # Fetching key pricing points
                last_price = hist['Close'].iloc[-1]
                prev_close = t.info.get('previousClose', last_price) # Fallback to last_price
                
                # Calculate daily change if prev_close exists
                change_pct = ((last_price - prev_close) / prev_close * 100) if prev_close else 0.0

                market_stats[ticker] = {
                    "price": round(last_price, 2),
                    "change_pct": round(change_pct, 2),
                    "currency": t.info.get('currency', 'USD')
                }
            except Exception as e:
                logger.error(f"Error fetching data for {ticker}: {e}")
                market_stats[ticker] = {"error": str(e)}

        return market_stats

if __name__ == "__main__":
    sensor = YFinanceSensor(["QQQ", "^VIX", "NVDA"])
    print(sensor.fetch_market_data())
