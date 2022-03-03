
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
   


