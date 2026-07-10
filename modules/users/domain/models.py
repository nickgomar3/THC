from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String, nullable=False)
    pokemons = relationship("UserPokemon", backref="user", cascade="all, delete-orphan")
    

class UserPokemon(Base):
    __tablename__ = "user_pokemons"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pokemon_id = Column(Integer, nullable=False)