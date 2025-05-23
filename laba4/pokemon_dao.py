from models import FirePokemon, WaterPokemon
from database import Session

def get_pokemons_by_trainer(trainer_id):
    session = Session()
    try:
        fire_pokemons = session.query(FirePokemon).filter_by(trainer_id=trainer_id).all()
        water_pokemons = session.query(WaterPokemon).filter_by(trainer_id=trainer_id).all()
        return fire_pokemons + water_pokemons
    finally:
        session.close()

def delete_pokemon_by_id(pokemon_id):
    session = Session()
    try:
        pokemon = session.query(FirePokemon).get(pokemon_id) or session.query(WaterPokemon).get(pokemon_id)
        if pokemon:
            session.delete(pokemon)
            session.commit()
            return True
        return False
    finally:
        session.close()

def update_pokemon(pokemon_id, **kwargs):
    session = Session()
    try:
        pokemon = session.query(FirePokemon).get(pokemon_id) or session.query(WaterPokemon).get(pokemon_id)
        if pokemon:
            for key, value in kwargs.items():
                if hasattr(pokemon, key):
                    setattr(pokemon, key, value)
            session.commit()
            return True
        return False
    finally:
        session.close()

def create_fire_pokemon(name, health, damage, fire_power, fire_resistance, trainer_id):
    session = Session()
    try:
        pokemon = FirePokemon(
            name=name,
            health=health,
            damage=damage,
            firepower=fire_power,
            fireresistance=fire_resistance,
            trainer_id=trainer_id
        )
        session.add(pokemon)
        session.commit()
        return pokemon
    finally:
        session.close()

def create_water_pokemon(name, health, damage, water_power, water_resistance, trainer_id):
    session = Session()
    try:
        pokemon = WaterPokemon(
            name=name,
            health=health,
            damage=damage,
            waterpower=water_power,
            waterresistance=water_resistance,
            trainer_id=trainer_id
        )
        session.add(pokemon)
        session.commit()
        return pokemon
    finally:
        session.close()
