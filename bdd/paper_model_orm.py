from sqlalchemy import Column, Integer, String

from .manager_bdd import get_base

"""
Pdf is an ORM class in order to store data and metadata of a pdf inside a database
"""


class PapierORM(get_base()):
    __tablename__ = "arxivpaper"
    doi = Column("doi", String, primary_key=True)
    title = Column("title", String)
    authors = Column("authors", String)
    link = Column("link", String(255))
    summary = Column("summary", String(255))
    data_published = Column("data_published", String(255))


    def __init__(self,doi,title,authors,link,summary,date_published):

        self.doi = doi, 
        self.title = title,
        self.authors = authors,
        self.link = link,
        self.summary = summary, 
        self.date_published = date_published
   
