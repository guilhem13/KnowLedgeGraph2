from sqlalchemy import Column, Integer, String
from .manager_bdd import Base


class PapierORM(Base):

    """
    PapierORM is an ORM class in order to store data and metadata of an article inside a database
    """

    __tablename__ = "arxivpaper"
    doi = Column("doi", String, primary_key=True)
    title = Column("title", String)
    authors = Column("authors", String)
    link = Column("link", String)
    summary = Column("summary", String)
    datepublished = Column("data_published", String)

    def __init__(self, doi, title, authors, link, summary, datepublished):

        self.doi = doi
        self.title = title
        self.authors = authors
        self.link = link
        self.summary = summary
        self.datepublished = datepublished
