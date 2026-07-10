from fastapi import APIRouter, Depends
from modules.users.application.service import UserService
from modules.users.dependencies import get_user_service
from .schemas import UserCreateDTO, UserPrivate, UserPublic, UserUpdateDTO


router = APIRouter()


@router.get("/", response_model=list[UserPublic])
async def get_users(service: UserService = Depends(get_user_service)):
    return await service.get_users()


@router.get("/{user_id}", response_model=UserPublic)
async def get_user_by_id(
    user_id: int, 
    service: UserService = Depends(get_user_service)
):
    return await service.get_user_by_id(user_id)


@router.post("/", response_model=UserPrivate)
async def create_user(
    user: UserCreateDTO,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(user.username, user.email, user.password, user.pokemons)


@router.put("/{user_id}", response_model=UserPrivate)
async def update_user(
    user_id: int,
    user: UserUpdateDTO,
    service: UserService = Depends(get_user_service)
):
    return await service.update_user(user_id, user.username, user.email, user.pokemons)


@router.delete("/{user_id}", response_model=UserPublic)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return await service.delete_user(user_id)