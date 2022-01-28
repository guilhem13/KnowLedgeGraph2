from sqlalchemy import Column, Integer, String

from . import modelbdd

"""
Pdf is an ORM class in order to store data and metadata of a pdf inside a database

"""


class Pdf(modelbdd.Base):
    __tablename__ = "pdftext"
    id = Column("id", String, primary_key=True)
    name = Column("name", String)
    data = Column("data", String)
    creationdate = Column("date", String(255))
    author = Column("author", String(255))
    title = Column("title", String(255))
    creator = Column("creator", String(255))
    producer = Column("producer", String(255))
    subject = Column("subject", String(255))
    keywords = Column("keywords", String(255))
    number_of_pages = Column("number_of_pages", Integer)
    title_file = Column("title_file", String(255))
    timestamp_uploading = Column("timestamp_uploading", String(255))

    def __init__(
        self,
        name,
        data,
        title,
        creationdate,
        author,
        creator,
        producer,
        subject,
        keywords,
        number_of_pages,
        title_file,
        timestamp_uploading,
    ):
        self.name = name
        self.data = data
        self.title = title
        self.creationdate = creationdate
        self.author = author
        self.creator = creator
        self.producer = producer
        self.subject = subject
        self.keywords = keywords
        self.number_of_pages = number_of_pages
        self.title_file = title_file
        self.timestamp_uploading = timestamp_uploading
