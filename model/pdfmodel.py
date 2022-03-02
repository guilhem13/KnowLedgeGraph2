
class Pdf():
    name = None
    data = None
    creationdate = None
    author = None
    title = None
    creator = None
    producer = None
    subject = None
    keywords = None
    number_of_pages = None
    title_file = None
    timestamp_uploading = None

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
