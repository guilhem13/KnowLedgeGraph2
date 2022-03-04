from sqlalchemy import Column, Integer, String

from . import model_bdd

"""
Pdf is an ORM class in order to store data and metadata of a pdf inside a database
"""


class PapierORM(model_bdd.Base):
    __tablename__ = "arxivpaper"
    doi = Column("doi", String, primary_key=True)
    title = Column("title", String)
    authors = Column("authors", String)
    link = Column("link", String(255))
    summary = Column("summary", String(255))
    data_published = Column("data_published", String(255))


   class Papier():

    title = None,
    doi = None
    authors = None,
    link = None,
    summary = None,
    date_published= None, 
    entities_from_reference = None,
    entities_include_in_text = None, 
    subject = None
    url_in_text = None
    doi_in_text = None  

    def __init__(self,title,doi,authors,link,summary,date_published):

        self.title = title,
        self.doi = doi, 
        self.authors = authors,
        self.link = link,
        self.summary = summary, 
        self.date_published = date_published
   
