from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Trainer(Base):
    __tablename__ = 'trainer'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    pokemons = relationship("Pokemon", back_populates="trainer")