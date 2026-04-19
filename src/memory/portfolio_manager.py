import yaml
import os
from loguru import logger

class PortfolioManager:
    def __init__(self, config_path: str = "portfolio.yaml"):
        self.config_path = config_path
        self.portfolio = self._load_portfolio()

    def _load_portfolio(self):
        """Loads and parses the portfolio YAML file."""
        if not os.path.exists(self.config_path):
            logger.warning(f"Portfolio config not found at {self.config_path}. Falling back to empty state.")
            return {"cash_usd": 0.0, "positions": [], "risk_management": {}}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                logger.info(f"Successfully loaded portfolio from {self.config_path}")
                return data or {}
        except Exception as e:
            logger.error(f"Error reading portfolio config: {e}")
            return {"cash_usd": 0.0, "positions": [], "risk_management": {}}

    def get_all_positions(self):
        """Returns all positions."""
        return self.portfolio.get("positions", [])

    def get_stock_positions(self):
        """Returns only stock positions."""
        return [p for p in self.get_all_positions() if p.get("type") == "stock"]

    def get_crypto_positions(self):
        """Returns only crypto positions."""
        return [p for p in self.get_all_positions() if p.get("type") == "crypto"]

    def get_risk_parameters(self):
        """Returns risk management parameters."""
        return self.portfolio.get("risk_management", {})

    def get_cash_balance(self):
        """Returns the current cash balance."""
        return self.portfolio.get("cash_usd", 0.0)

if __name__ == "__main__":
    pm = PortfolioManager("portfolio.yaml.example")
    print(pm.get_all_positions())
