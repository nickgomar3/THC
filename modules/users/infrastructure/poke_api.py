import httpx
from gateway.ipoke_api import IPokeAPIGateway

from core.config import settings


class PokeAPIClient(IPokeAPIGateway):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.url = settings.pokeapi_url
        
    
    async def get_pokemon_name(self, pokemon_id: int) -> str:
        # Ya no abrimos el cliente aquí, usamos el que nos inyectaron
        response = await self.client.get(f"{self.url.rstrip('/')}/{pokemon_id}")
        response.raise_for_status()
        return response.json()["name"]
    
    
    """async def get_pokemon_name(self, pokemon_id: int) -> str:
        async with httpx.AsyncClient() as client:
            
            
            url = f"{settings.pokeapi_url}/{pokemon_id}"
            
            response = await client.get(url)
            response.raise_for_status()
            return response.json()["name"]"""