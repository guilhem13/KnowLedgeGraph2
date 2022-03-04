import os
import arxiv 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from controller import Data
from .paper_model_orm import PapierORM

#basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///bdd/bddarxiv.db?check_same_thread=False"  # ajout de false pour la gestion de probleme des threads
Base = declarative_base()

def get_base(): 
    return Base 

# creation of a session connected with the database basededonnepdf.db
def session_creator():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    return session()

def feed_bdd (paper, nb_paper, session):

    client_arxiv = arxiv.Client(page_size =nb_paper,delay_seconds = 3,num_retries = 5)
    for result in client_arxiv.results(arxiv.Search(query = "cat:cs.AI",max_results =nb_paper,sort_by = arxiv.SortCriterion.SubmittedDate,)):
        p = PapierORM(result.title,Data.get_doi(result.entry_id),Data.process_authors(result.authors),result.pdf_url,result.summary,result.published)
        if session.query(PapierORM).filter(PapierORM.doi == p.doi).scalar() == False: 
            session.add(p)
            session.commit()
        
        