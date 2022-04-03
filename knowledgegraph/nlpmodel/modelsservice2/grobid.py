import xml.etree.ElementTree as ET

from grobid.client import GrobidClient

from knowledgegraph.models import Entity


class Grobid:

    """
    Grobid client object to manage response from grobid server
    """
    path = None

    def __init__(self, path):
        self.path = path

    def get_entities(self):

        client = GrobidClient("localhost", "8070")
        rsp = client.serve("processReferences", self.path, consolidate_header=1)

        result = []
        tree = ET.parse("resultat_tei.xml")
        root = tree.getroot()
        for child in root.findall("./text/back/div/listBibl/biblStruct/analytic"):
            for author in child.findall("author"):
                for person in author:
                    if person.tag == "persName":
                        for caract in person.getchildren():
                            p = Entity()
                            if caract.tag == "forename":
                                p.set_prenom(caract.text)
                            if caract.tag == "surname":
                                p.set_nom(caract.text)
                            result.append(p)

        return result
