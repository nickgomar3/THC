from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)
    

class UserCreateDTO(UserBase):
    password: str = Field(min_length=8)
    pokemons: list[int] = Field(default_factory=list)


class UserUpdateDTO(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    pokemons: list[int] | None = Field(default=None)


class PokemonPublic(BaseModel):
    name: str


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    pokemons: list[PokemonPublic]


class UserPrivate(UserPublic):
    email: EmailStr
    pokemons: list[int]