import factory
from modules.users.domain.models import User, UserPokemon


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None # It'll be injected in the test

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = "hashed_password"
    

class UserPokemonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserPokemon
        sqlalchemy_session = None

    pokemon_id = factory.Faker("random_int", min=1, max=151)