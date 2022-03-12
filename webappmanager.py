import multiprocessing as mp
import arxiv 
from knowledgegraph.controller import Pipeline
from bdd.paper_model_orm import PapierORM
from knowledgegraph.controller import Data
from knowledgegraph.owl import ontology
from knowledgegraph.models import Papier , Entity
import ast

"""
route --- getner part 
"""

ALLOWED_EXTENSIONS = {"pdf"}  

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

"""
route --- feedbdd part 
"""

def feed_bdd (nb_paper, session):

    client_arxiv = arxiv.Client(page_size =nb_paper,delay_seconds = 3,num_retries = 5)
    converter = Data(nb_paper)
    for result in client_arxiv.results(arxiv.Search(query = "cat:cs.AI",max_results =nb_paper,sort_by = arxiv.SortCriterion.SubmittedDate,)):
        list_of_entites = converter.process_authors(result.authors)
        list_of_entites = [x.__dict__ for x in list_of_entites]
        p = PapierORM(converter.get_doi(result.entry_id) , result.title , str(list_of_entites) , result.pdf_url, result.summary , str(result.published))
        if session.query(PapierORM).first() ==None : 
            session.add(p)
            session.commit()
        else:   
            if session.query(PapierORM).filter(PapierORM.doi == p.doi).scalar() is None: 
                session.add(p)
                session.commit()
                
"""
route --- generate pipeline 
"""
def generate_pipeline(nb_paper): 
    nb_paper_to_request = int(nb_paper)
    block_arxiv_size = 5
    arxiv_data = Data(nb_paper_to_request).get_set_data()
    papiers= []
    for i in range(0,len(arxiv_data),block_arxiv_size):
        print(i) 
        papiers+= arxiv_route_main_function(arxiv_data[i:i+block_arxiv_size])
    owl = ontology.Ontology()
    for papier in papiers: 
        owl.add_papier(papier)
    owl.save('result.owl')

def arxiv_route_main_function(block_paper):

    p = Pipeline("https://export.arxiv.org/pdf/",0)
    out_queue = mp.Queue()
    batch_size = 5
    return p.make_traitement_pipeline(block_paper, out_queue, batch_size)

"""
route --- generate pipeline 
"""

def convert_dict_to_entities(stringdict):
    entities_list = []
    res = ast.literal_eval(stringdict)
    for item in res: 
        p = Entity()   
        p.set_prenom(item['prenom'])
        p.set_nom(item['nom'])
        entities_list.append(p)

    return entities_list

def pipeline_from_bdd(session): 
    papers = session.query(PapierORM).all()
    paper_list = []
    for paper in papers :
        paper_list.append(Papier(paper.title,paper.doi,convert_dict_to_entities(paper.authors),paper.link,paper.summary,paper.data_published))
    
    return True