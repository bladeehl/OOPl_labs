from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from trainer_model import Base

DATABASE_URL = "postgresql+psycopg2://postgres:osuosu454@localhost:5432/pokeJava"

engine = create_engine(DATABASE_URL, echo=False)
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
