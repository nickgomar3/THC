import httpx
from gateway.ipoke_api import IPokeAPIGateway

from core.config import settings


class PokeAPIClient(IPokeAPIGateway):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        # self.url = settings.pokeapi_url
        self.url = settings.pokeapi_url.rstrip("/")
        
    
    async def get_pokemon_name(self, pokemon_id: int) -> str:
        # Esto armará correctamente: https://pokeapi.co/api/v2/pokemon/25
        response = await self.client.get(f"{self.url}/{pokemon_id}")
        response.raise_for_status()
        return response.json()["name"]
    
    
    """async def get_pokemon_name(self, pokemon_id: int) -> str:
        async with httpx.AsyncClient() as client:
            
            
            url = f"{settings.pokeapi_url}/{pokemon_id}"
            
            response = await client.get(url)
            response.raise_for_status()
            return response.json()["name"]"""