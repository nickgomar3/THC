import pytest
import httpx

from modules.users.domain import User, UserPokemon
from core.config import settings


@pytest.mark.anyio
async def test_create_user(client, db_session):
    data = {"username": "nico", "email": "nico@gmail.com", "password": "12345678", "pokemons": [25]}

    response = await client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["username"] == "nico"


@pytest.mark.anyio
async def test_get_user(client, db_session, mock_pokeapi):
    user = User(username="nico", email="nico.get@test.com", password="securepassword")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    pokemon = UserPokemon(user_id=user.id, pokemon_id=25)
    db_session.add(pokemon)
    await db_session.commit()
    
    mock_pokeapi.get(f"{settings.pokeapi_url}/25").mock(
        return_value=httpx.Response(200, json={"name": "pikachu"})
    )
    
    response = await client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["pokemons"][0]["name"] == "pikachu"


@pytest.mark.anyio
async def test_update_user(client, db_session):
    user = User(username="nico", email="nico.update@test.com", password="securepassword")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    update_data = {"username": "nico_nuevo", "email": "nuevo@test.com", "pokemons": []}
    response = await client.put(f"/users/{user.id}", json=update_data)
    
    assert response.status_code == 200
    assert response.json()["username"] == "nico_nuevo"


@pytest.mark.anyio
async def test_delete_user(client, db_session):
    user = User(username="borrar", email="nico.delete@test.com", password="securepassword")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    response = await client.delete(f"/users/{user.id}")
    assert response.status_code == 200
    
    resp_get = await client.get(f"/users/{user.id}")
    assert resp_get.status_code == 404