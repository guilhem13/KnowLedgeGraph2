import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    basedir, "basededonneepdf.db?check_same_thread=False"
)  # ajout de false pour la gestion de probleme des threads
UPLOAD_FOLDER = basedir
Base = declarative_base()


# creation of a session connected with the database basededonnepdf.db
def session_creator():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    return session()