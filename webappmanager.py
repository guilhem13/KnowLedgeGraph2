import multiprocessing as mp
import arxiv 
from knowledgegraph.controller import Pipeline

ALLOWED_EXTENSIONS = {"pdf"}  

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def arxiv_route_main_function(block_paper):

    p = Pipeline("https://export.arxiv.org/pdf/",0)
    out_queue = mp.Queue()
    batch_size = 5
    return p.make_traitement_pipeline(block_paper, out_queue, batch_size)

def feed_bdd (paper, nb_paper, session):

    client_arxiv = arxiv.Client(page_size =nb_paper,delay_seconds = 3,num_retries = 5)
    for result in client_arxiv.results(arxiv.Search(query = "cat:cs.AI",max_results =nb_paper,sort_by = arxiv.SortCriterion.SubmittedDate,)):
        p = PapierORM(result.title,Data.get_doi(result.entry_id),Data.process_authors(result.authors),result.pdf_url,result.summary,result.published)
        if session.query(PapierORM).filter(PapierORM.doi == p.doi).scalar() == False: 
            session.add(p)
            session.commit()