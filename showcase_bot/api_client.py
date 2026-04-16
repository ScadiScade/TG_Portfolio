import aiohttp
from config import API_KEY

class ExchangeAPIClient:
    def __init__(self):
        self.base_url = "https://open.er-api.com/v6/latest/"
        
    async def get_rates(self, base_currency: str = "USD") -> dict:
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{self.base_url}{base_currency.upper()}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("rates", {})
                    return {}
            except Exception as e:
                print(f"API Request failed: {e}")
                return {}

    async def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        rates = await self.get_rates(from_currency)
        if not rates or to_currency.upper() not in rates:
            return None
            
        rate = rates[to_currency.upper()]
        return round(amount * rate, 2)
