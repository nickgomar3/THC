from abc import ABC, abstractmethod


class IPokeAPIGateway(ABC):
    
    @abstractmethod
    async def get_pokemon_name(self, pokemon_id: int) -> str:
        pass