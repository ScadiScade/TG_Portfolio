import aiohttp
from config import API_KEY

class ExchangeAPIClient:
    def __init__(self):
        # We will use a free mock api for the sake of the portfolio project.
        # In a real scenario, this would point to a real API endpoint like https://api.exchangerate-api.com/v4/latest/
        self.base_url = "https://open.er-api.com/v6/latest/"
        
    async def get_rates(self, base_currency: str = "USD") -> dict:
        """Fetch latest exchange rates."""
        async with aiohttp.ClientSession() as session:
            try:
                # API documentation: https://www.exchangerate-api.com/docs/free
                url = f"{self.base_url}{base_currency.upper()}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("rates", {})
                    else:
                        print(f"API Error: {response.status}")
                        return {}
            except Exception as e:
                print(f"API Request failed: {e}")
                return {}

    async def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert an amount from one currency to another."""
        rates = await self.get_rates(from_currency)
        if not rates or to_currency.upper() not in rates:
            return None
            
        rate = rates[to_currency.upper()]
        return round(amount * rate, 2)
