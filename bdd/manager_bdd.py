from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "sqlite:///bdd/bddarxiv.db?check_same_thread=False"  # ajout de false pour la gestion de probleme des threads
Base = declarative_base()


# creation of a session connected with the database bddarxiv.db
def session_creator():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    return session()
