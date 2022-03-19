import requests
from xml.etree.ElementTree import fromstring, ElementTree
from knowledgegraph.models import Entity

class Cermine():

    path = None

    def __init__(self,path):
        self.path = path
    
    def request_service(self, path): 

        headers = {'Content-Type': 'application/binary'}
        data = open(path, 'rb').read()
        response = requests.post('http://localhost:8072/extract.do', headers=headers, data=data)
        return response 
    
    def get_entities(self): 
        response = self.request_service(self.path)
        tree =  ElementTree(fromstring(response.content.decode("utf-8", errors="replace")))
        root = tree.getroot()
        result =[]
        for child in root.find("./back/ref-list"):
            for persons in child.findall('mixed-citation/string-name'):
                for person in persons:
                    p = Entity()
                    if person.tag == 'given-names':
                        if person.text is not None: 
                            p.set_prenom(person.text)
                        else:
                            p.set_prenom("NoPrenom")
                    if person.tag =='surname': 
                        if person.text is not None: 
                            p.set_nom(person.text)
                        else:
                            p.set_nom("Nonom")
                    if p.nom[0] is None :
                        p.set_nom("Nonom")
                    if p.prenom is None: 
                        p.set_nom("NoPrenom")
                    p.set_name(p.nom[0]+p.prenom[0])
                    result.append(p)
        print(len(result))           
        return result
       