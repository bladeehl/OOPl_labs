from trainer_model import Trainer
from database import Session

def get_all_trainers():
    session = Session()
    try:
        return session.query(Trainer).all()
    finally:
        session.close()

def get_trainer_by_id(trainer_id):
    session = Session()
    try:
        return session.query(Trainer).get(trainer_id)
    finally:
        session.close()

def create_trainer(name):
    session = Session()
    try:
        trainer = Trainer(name=name)
        session.add(trainer)
        session.commit()
        return trainer
    finally:
        session.close()

def delete_trainer(trainer_id):
    session = Session()
    try:
        trainer = session.query(Trainer).get(trainer_id)
        if trainer:
            session.delete(trainer)
            session.commit()
            return True
        return False
    finally:
        session.close()

def update_trainer(trainer_id, new_name):
    session = Session()
    try:
        trainer = session.query(Trainer).get(trainer_id)
        if trainer:
            trainer.name = new_name
            session.commit()
            return True
        return False
    finally:
        session.close()
