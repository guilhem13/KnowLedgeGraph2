from .modelsservice2.cermine import Cermine
from .modelsservice2.grobid import Grobid

class ServiceTwo():

    path = None

    def __init__(self,path):
        self.path= path
    
    def __eq__(self, other):
        return self.prenom==other.prenom\
            and self.nom==other.nom

    def get_references(self): 
        #grobid_result = Grobid(self.path).get_entities()
        cermine_result = Cermine(self.path).get_entities()
        #murge_list = list(set(grobid_result + cermine_result))
        return cermine_result
