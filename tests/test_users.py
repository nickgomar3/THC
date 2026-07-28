import pytest
import httpx
from httpx import AsyncClient

from .factories import UserFactory, UserPokemonFactory
from core.config import settings


@pytest.mark.anyio
async def test_create_user(client, db_session):
    data = {"username": "nico", "email": "nico@gmail.com", "password": "12345678", "pokemons": [25]}

    response = await client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["username"] == "nico"


@pytest.mark.anyio
async def test_get_user(client, db_session, mock_pokeapi):
    user = UserFactory(username="nico")
    UserPokemonFactory(user=user, pokemon_id=25)
    
    # El mock intercepta la llamada interna del servicio
    # mock_pokeapi.get("/25").mock(return_value=httpx.Response(200, json={"name": "pikachu"}))

    # Interceptamos la URL completa que genera el cliente
    mock_pokeapi.get(f"{settings.pokeapi_url.rstrip('/')}/25").mock(
        return_value=httpx.Response(200, json={"name": "pikachu"})
    )
    
    response = await client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["pokemons"][0]["name"] == "pikachu"


@pytest.mark.anyio
async def test_update_user(client, db_session):
    user = UserFactory(username="nico")
    
    update_data = {"username": "nico_nuevo", "email": "nuevo@test.com", "pokemons": []}
    response = await client.put(f"/users/{user.id}", json=update_data)
    
    assert response.status_code == 200
    assert response.json()["username"] == "nico_nuevo"


@pytest.mark.anyio
async def test_delete_user(client, db_session):
    user = UserFactory()
    
    response = await client.delete(f"/users/{user.id}")
    assert response.status_code == 200
    
    # Verificar que ya no existe
    resp_get = await client.get(f"/users/{user.id}")
    assert resp_get.status_code == 404