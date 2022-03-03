from owlready2 import get_ontology
from xml.sax.saxutils import escape

class Ontology():

    def __init__(self):
        self.template_onto = get_ontology("file://owl/onto3.owl").load()
        self.foaf = self.template_onto.get_imported_ontologies().first().load()
    
                
    def add_papier(self, papier):
         with self.template_onto:
            document_object = self.template_onto.Papier(escape(papier.doi[0]))
            document_object.doi.append(papier.doi[0])
            document_object.doi.append(papier.title[0])
            document_object.doi.append(papier.link[0]) 
            
            for entite in papier.authors[0]: 
                author_object = self.template_onto.Auteur(entite.nom)
                author_object.firstName.append(entite.prenom)
                author_object.lastName.append(entite.nom)
                author_object.a_ecrit.append(document_object)
                document_object.a_comme_auteur.append(author_object)
            
            for reference in papier.entities_from_reference: 
                person = self.foaf.Person(reference.nom)
                person.firstName.append(reference.prenom)
                person.lastName.append(reference.nom)
                person.est_reference_dans.append(document_object)
                document_object.a_comme_reference.append(person)

    def save(self,filepath):
        
        self.template_onto.save(filepath)
    

    def get_ontology(self):
        return self.template_onto

