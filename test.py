from bdd.paper_model_orm import PapierORM
from bdd.manager_bdd import session_creator
from knowledgegraph.models import Papier , Entity
from knowledgegraph.controller import Data
import ast


session = session_creator()
# User is the name of table that has a column name

def convert_dict_to_entities(stringdict):
    entities_list = []
    res = ast.literal_eval(stringdict)
    for item in res: 
        p = Entity()   
        p.set_prenom(item['prenom'])
        p.set_nom(item['nom'])
        entities_list.append(p)

    return entities_list

papers = session.query(PapierORM).all()
paper_list = []
for paper in papers :
    paper_list.append(Papier(paper.title,paper.doi,convert_dict_to_entities(paper.authors),paper.link,paper.summary,paper.data_published))



