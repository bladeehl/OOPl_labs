from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from trainer_model import Base

class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    health = Column(Integer, nullable=False)
    damage = Column(Integer, nullable=False)
    trainer_id = Column(Integer, ForeignKey('trainer.id'), nullable=False)

    immune_next_turn = False
    damage_reduction = 0
    counter_damage = 0
    last_attacker = None

    type = Column(String)
    trainer = relationship("Trainer", back_populates="pokemons")

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'pokemon',
        'with_polymorphic': '*'
    }

    def attack(self, target):
        target.last_attacker = self
        target.take_damage(self.damage)

    def take_damage(self, dmg):
        if self.immune_next_turn:
            self.immune_next_turn = False
            return

        dmg -= self.damage_reduction
        if dmg > 0:
            self.health -= dmg
            if self.health < 0:
                self.health = 0
            if self.counter_damage > 0 and self.last_attacker:
                self.last_attacker.take_damage(self.counter_damage)
                self.counter_damage = 0

    def ability(self):
        pass

    def evolve(self):
        pass

    def defend(self):
        pass


class FirePokemon(Pokemon):
    __tablename__ = 'firepokemon'
    id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True)
    fireresistance = Column(Integer)
    firepower = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'Fire',
    }

    def ability(self):
        self.damage += 5

    def fire_ball(self, target):
        target.take_damage(self.firepower + 20)

    def fire_thorns(self):
        self.counter_damage = self.fireresistance // 4

    def evolve(self):
        self.damage = int(self.damage * 1.5)

    def defend(self):
        self.damage_reduction = self.fireresistance // 3


class WaterPokemon(Pokemon):
    __tablename__ = 'waterpokemon'
    id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True)
    waterresistance = Column(Integer)
    waterpower = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'Water',
    }

    def ability(self):
        self.health += 50

    def water_hide(self):
        self.immune_next_turn = True

    def wave_attack(self, target):
        target.take_damage(self.waterpower + 10)

    def evolve(self):
        self.health *= 2

    def defend(self):
        self.damage_reduction = self.waterresistance // 2