from xml.etree.ElementTree import ElementTree, fromstring

import requests

from knowledgegraph.models import Entity


class Cermine:

    """
    Cermine client object to manage response from cermine server
    """

    path = None

    def __init__(self, path):
        self.path = path

    def request_service(self, path):

        headers = {"Content-Type": "application/binary"}
        data = open(path, "rb").read()
        response = requests.post(
            "http://localhost:8072/extract.do", headers=headers, data=data
        )
        return response

    def get_entities(self):
        response = self.request_service(self.path)
        print(self.path)
        tree = ElementTree(
            fromstring(response.content.decode("utf-8", errors="replace"))
        )
        root = tree.getroot()
        result = []
        forbidden_list =['Analysis','Pattern','Recognition','Vision','Computer','Learning','Machine','Artificial','Intelligence','Computer','Science','Representation','Continuous','Facilities','Council','Dominican','Republic','Multiagent','Systems','Autonomous','Agents','Biometrics','Lab','Physics','Neural','Systems','Mathematics','Mathematical','Computational','Meta-Learning',"Parameter","Available","Online","Practical","Momentum","AGCN","AGCN","Engineering","Data","Retrieval","Programming","Research","Verification","Network"]
        for child in root.find("./back/ref-list"):
            for persons in child.findall("mixed-citation/string-name"):
                for person in persons:
                    p = Entity()
                    p.set_nom("Nonom")
                    p.set_prenom("Noprenom")
                    if person.tag == "given-names":
                        if person.text is not None:
                            p.set_prenom(person.text.strip())
                        else:
                            p.set_prenom("NoPrenom")
                    if person.tag == "surname":
                        if person.text is not None:
                            p.set_nom(person.text.strip())
                        else:
                            p.set_nom("Nonom")
                    p.set_name(p.prenom + p.nom)

                    if p.nom not in forbidden_list and p.prenom not in forbidden_list:
                        result.append(p)

        print("Cermine a trouvé un nombre d'entités de "+str(len(result)))
        return result
