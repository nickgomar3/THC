from unicodedata import name

from gateway import IPokeAPIGateway
from modules.users.domain import User, UserPokemon, IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork, poke_gateway: IPokeAPIGateway):
        self.uow = uow
        self.poke_gateway = poke_gateway


    async def get_users(self):
        async with self.uow:
            users = await self.uow.users.get()
            
            # From users list to DTOs
            result = []
            for user in users:
                result.append({
                    "id": user.id,
                    "username": user.username,
                    "pokemons": [{"name": await self.poke_gateway.get_pokemon_name(p.pokemon_id)} 
                                 for p in user.pokemons]
                })
                
            return result


    async def get_user_by_id(self, user_id: int):
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            
            if not user:
                raise Exception("User not found")
            
            pokemons_with_names = []
            for p in user.pokemons:
                name = await self.poke_gateway.get_pokemon_name(p.pokemon_id)
                pokemons_with_names.append({"name": name})
            
            return {
                "id": user.id,
                "username": user.username,
                "pokemons": pokemons_with_names
            }
        
        
    async def create_user(self, username: str, email: str, password: str, pokemon_ids: list[int]):
        async with self.uow:
            
            user_pokemon = [UserPokemon(pokemon_id=pid) for pid in pokemon_ids]
            
            user = User(username=username, email=email, password=password, pokemons=user_pokemon)
            
            await self.uow.users.add(user)
            await self.uow.commit()
            
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "pokemons": pokemon_ids
            }
    
    
    async def update_user(self, user_id: int, username: str, email: str, pokemon_ids: list[int]):
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            
            if not user:
                raise Exception("User not found")
            
            user.username = username
            user.email = email
            
            user.pokemons = [UserPokemon(pokemon_id=pid) for pid in pokemon_ids]
            
            await self.uow.users.update(user)
            await self.uow.commit()
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "pokemons": pokemon_ids
            }
            

    async def delete_user(self, user_id: int):
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            
            if not user:
                raise Exception("User not found")
            
            await self.uow.users.delete(user)
            await self.uow.commit()
            return user