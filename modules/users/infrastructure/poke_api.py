import httpx
from gateway.ipoke_api import IPokeAPIGateway

from core.config import settings


class PokeAPIClient(IPokeAPIGateway):
    
    async def get_pokemon_name(self, pokemon_id: int) -> str:
        async with httpx.AsyncClient() as client:
            #response = await client.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
            
            url = f"{settings.pokeapi_url}/{pokemon_id}"
            
            response = await client.get(url)
            response.raise_for_status()
            return response.json()["name"]