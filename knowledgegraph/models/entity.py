
class Entity():

    prenom = None,
    nom = None
    name = None, #TODO avant yavait le doi à voir si c'est ok pour le garder ou le laisser   

    def __init__(self):

        pass

    # setter method
    def set_prenom(self, x):
        self.prenom = x    
    
    def set_nom(self, x):
        self.nom = x

    def set_name(self, x):
        self.name = x  

    def __eq__(self, other): 
        equals = False
        if not isinstance(other, Entity):
            return NotImplemented
        if self.nom == other.nom: 
            #if other.prenom in self.prenom: 
            equals = True

        return equals
   