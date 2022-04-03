from typing import Type
import requests
import json 
from knowledgegraph.models.entity import Entity

def convert_json_to_entities(slistjson):
    entities_list = []
    for item in slistjson:
        item_ = json.loads(json.dumps(item))
        p = Entity()
        p.set_prenom(item_["prenom"].strip())
        p.set_nom(item_["nom"].strip())
        p.set_name(item_["name"])
        entities_list.append(p)

    return entities_list


"""'papier_2':'https://export.arxiv.org/pdf/2203.06416v1',
    'papier_3':'https://export.arxiv.org/pdf/2203.07372v1'"""

json_data = {
            'papier_1':'https://export.arxiv.org/pdf/2203.00193v2',
            'papier_2':'https://export.arxiv.org/pdf/2203.00192v1',
            'papier_3':'https://export.arxiv.org/pdf/2203.00190v3',  
            'papier_4':'https://export.arxiv.org/pdf/2203.00183v2',
            'papier_5':'https://export.arxiv.org/pdf/2203.00160v1'
            }

import ast 
headers = {'content-type': 'application/json'}
r = requests.post(url = "http://localhost:5000/get/entities", data =json.dumps(json_data), headers =headers)

print(type(r.text))
a = ast.literal_eval(r.text)
print(type(a))
print(len(a))
for item in a : 
    b = json.loads(item)
    
    print(b['entities_from_reference'])
    print(type(b['entities_from_reference'])) 
    c = convert_json_to_entities(b['entities_from_reference'])
    print(b)
            
  

"""
for item in json.loads(r.text)[0]: 
    print(item['link'])"""