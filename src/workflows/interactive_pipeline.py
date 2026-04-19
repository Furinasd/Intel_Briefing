import logging
from typing import Dict, Any

from src.memory.portfolio_manager import PortfolioManager
from src.sensors.yfinance_sensor import YFinanceSensor
from src.sensors.crypto_sensor import CryptoSensor
from src.agents.ely_prompt_bus import ElyPromptBus

# Using the internal Gemini utility we already have
try:
    from src.utils.gemini_translator import _gemini_api_call
except ImportError:
    from utils.gemini_translator import _gemini_api_call

logger = logging.getLogger(__name__)

class InteractivePipeline:
    def __init__(self):
        self.portfolio_mgr = PortfolioManager()
        self.yf_sensor = YFinanceSensor()
        self.crypto_sensor = CryptoSensor()
        self.prompt_bus = ElyPromptBus()

    def process_query(self, user_message: str) -> str:
        """Processes an interactive user query through the Ely-Agent core."""
        logger.info(f"Processing CEO query: {user_message}")
        
        # 1. Fetch State
        portfolio_state = {
            "cash_usd": self.portfolio_mgr.get_cash_balance(),
            "positions": self.portfolio_mgr.get_all_positions(),
            "risk_management": self.portfolio_mgr.get_risk_parameters()
        }
        
        # 2. Fetch Sandbox Context (Sensors)
        market_stats = {}
        # Simple string matching to avoid fetching all if not needed, else fetch all for context.
        # For a sandbox, we fetch all to provide complete context.
        logger.info("Fetching real-time market data...")
        market_stats.update(self.yf_sensor.fetch_market_data())
        market_stats.update(self.crypto_sensor.fetch_market_data())

        # 3. Build prompts
        system_prompt = self.prompt_bus.get_system_prompt()
        user_prompt = self.prompt_bus.get_market_analysis_prompt(
            user_query=user_message,
            portfolio_context=portfolio_state,
            market_data=market_stats
        )

        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        # 4. Agent Reasoning Path
        logger.info("Sending context to LLM Engine...")
        response = _gemini_api_call(full_prompt, max_tokens=2048)
        
        if not response:
             return "I encountered an error connecting to the reasoning core. Please check API keys or connection."

        return response

if __name__ == "__main__":
    # Test Sandbox logic
    pipeline = InteractivePipeline()
    answer = pipeline.process_query("What is the current status of my portfolio vs the market today?")
    print(answer)
