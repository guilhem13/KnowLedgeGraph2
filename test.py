from threading import local
from bdd.paper_model_orm import PapierORM
from bdd.manager_bdd import session_creator
from knowledgegraph.models import Papier , Entity
from knowledgegraph.controller import Data
import ast
import glob , os 

"""
session = session_creator()
# User is the name of table that has a column name
papers = session.query(PapierORM).filter().limit(5).all()
print(len(papers))


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


p = Entity()   
p.set_prenom('prenom')
p.set_nom('nom')

a = Entity()   
a.set_prenom('prenom')
a.set_nom('nom')


files = glob.glob('knowledgegraph/file/*.pdf', recursive=True)

for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

from refextract import extract_references_from_file
references = extract_references_from_file('1810.04805.pdf')
listreferences = []
print(references)
for item in references:
    result =""
    if 'raw_ref' in item.keys(): 
        result.append(item['raw_ref'])
    if 'year' in item.keys():
        result += "&!&"
        result.append
    listreferences.append(item['raw_ref']) 

print(listreferences)
files = glob.glob('knowledgegraph/file/*.pdf', recursive=True)
for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))"""

dict ={}

persons_objects =[]
organisations_objects =['azeaaedaaeded','adedafdeda','afefefedcfdc']
lists = ['persons_objects','organisations_objects']
output = {}
data = {listname: locals()[listname] for listname in lists}


p = Entity()   
p.set_prenom('prenom1')
p.set_nom('nom1')

a = Entity()   
a.set_prenom('prenom1')
a.set_nom('nom1')


vv = []
vv.append(p)
vv.append(a)

data['Personne'] = []
for i in range(len(vv)): 
    data['Personne'].append(vv[i].__dict__)

dict['chunk_1']=data
print(dict)
"""
with open('abc.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)"""