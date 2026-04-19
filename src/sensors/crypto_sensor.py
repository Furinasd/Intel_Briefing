import requests
from loguru import logger
from typing import Dict, Any, List

class CryptoSensor:
    def __init__(self, coin_ids: List[str] = None):
        # CoinGecko uses specific IDs (e.g., 'bitcoin', 'ethereum')
        self.coin_ids = coin_ids or ["bitcoin", "ethereum", "solana"]
        self.base_url = "https://api.coingecko.com/api/v3"

    def fetch_market_data(self) -> Dict[str, Any]:
        """Fetches current market data from CoinGecko for configured coins."""
        logger.info(f"Fetching CoinGecko data for {self.coin_ids}")
        market_stats = {}
        
        # Simple/price endpoint is good for current price and 24h change
        ids_str = ",".join(self.coin_ids)
        url = f"{self.base_url}/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_change=true"
        
        try:
            # Added timeout and user-agent just in case
            headers = {"User-Agent": "Ely-Agent/1.1 (Private Research)"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for coin_id in self.coin_ids:
                if coin_id in data:
                    coin_data = data[coin_id]
                    market_stats[coin_id] = {
                        "price": round(coin_data.get("usd", 0.0), 2),
                        "change_pct": round(coin_data.get("usd_24h_change", 0.0), 2),
                        "currency": "USD"
                    }
                else:
                    logger.warning(f"No CoinGecko pricing data found for {coin_id}")
                    
        except Exception as e:
            logger.error(f"Error fetching CoinGecko data: {e}")
            for coin_id in self.coin_ids:
                 market_stats[coin_id] = {"error": str(e)}

        return market_stats

if __name__ == "__main__":
    sensor = CryptoSensor(["bitcoin", "solana"])
    print(sensor.fetch_market_data())
