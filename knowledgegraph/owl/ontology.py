from xml.sax.saxutils import escape

from owlready2 import get_ontology


class Ontology:

    """
    object which manage the creation and updating of ontology 
    """
    def __init__(self):
        self.template_onto = get_ontology("file://knowledgegraph/owl/onto10.owl").load()
        self.foaf = self.template_onto.get_imported_ontologies().first().load()

    def add_papier(self, papier):
        with self.template_onto:
            document_object = self.template_onto.Papier(escape(papier.doi))
            document_object.doi.append(papier.doi)
            document_object.doi.append(papier.title)
            document_object.doi.append(papier.link)

            for entite in papier.authors:
                author_object = self.template_onto.Auteur(escape(entite.name))
                author_object.firstName.append(entite.prenom)
                author_object.family_name.append(entite.nom)
                author_object.a_ecrit.append(document_object)
                document_object.a_comme_auteur.append(author_object)

            for reference in papier.entities_from_reference:
                person = self.foaf.Person(reference.name)
                person.firstName.append(reference.prenom)
                person.family_name.append(reference.nom)
                person.est_reference_dans.append(document_object)
                document_object.a_comme_reference.append(person)

            if len(papier.doi_in_text) > 0:
                for doiref in papier.doi_in_text:
                    doi_object = self.template_onto.Papier(escape(doiref))
                    document_object.a_cite_comme_papier.append(doi_object)

            if len(papier.url_in_text) > 0:
                for urlref in papier.url_in_text:
                    url_object = self.template_onto.lien_url(escape(urlref))
                    document_object.a_cite_comme_lien.append(url_object)

    def save(self, filepath):

        self.template_onto.save(filepath)

    def get_ontology(self):
        return self.template_onto
