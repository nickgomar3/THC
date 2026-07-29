import httpx
from gateway.ipoke_api import IPokeAPIGateway

from core.config import settings


class PokeAPIClient(IPokeAPIGateway):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.url = settings.pokeapi_url
        
    
    async def get_pokemon_name(self, pokemon_id: int) -> str:
        response = await self.client.get(f"{self.url}/{pokemon_id}")
        response.raise_for_status()
        return response.json()["name"]