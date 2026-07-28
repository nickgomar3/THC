import factory
from modules.users.domain.models import User, UserPokemon


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = "hashed_password"
    

class UserPokemonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = UserPokemon

    pokemon_id = factory.Faker("random_int", min=1, max=151)