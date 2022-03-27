from logging import exception

import nltk

from knowledgegraph.controller import Pipeline

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")
import ast
import glob
import multiprocessing as mp
import os

from bdd.manager_bdd import session_creator
from bdd.paper_model_orm import PapierORM
from knowledgegraph.controller import Data, Textprocessed
from knowledgegraph.models import Entity, Papier
from knowledgegraph.nlpmodel import (service_one_extraction,
                                     service_two_extraction)
from knowledgegraph.owl import ontology


def main_function(block_paper):

    p = Pipeline("https://export.arxiv.org/pdf/", 0)
    out_queue = mp.Queue()
    batch_size = 5
    return p.make_traitement_pipeline(block_paper, out_queue, batch_size)


def convert_dict_to_entities(stringdict):
    entities_list = []
    res = ast.literal_eval(stringdict)
    for item in res:
        p = Entity()
        p.set_prenom(item["prenom"])
        p.set_nom(item["nom"])
        p.set_name(item["prenom"] + item["nom"])
        entities_list.append(p)

    return entities_list


def services_manager(papier):

    servicetwocheckout = True
    try:
        print("use of cermine")
        result = service_two_extraction.ServiceTwo(
            "knowledgegraph/file/" + papier.doi + ".pdf"
        ).get_references()
        if len(papier.entities_from_reference) > 0:
            if len(result) > 0:
                for i in range(len(result)):
                    stop = False
                    j = 0
                    while j < (len(papier.entities_from_reference) - 1):
                        if stop == False:
                            if (
                                result[i].__eq__(papier.entities_from_reference[j])
                                == True
                            ):
                                stop = True
                        j += 1
                    if stop == False:
                        papier.entities_from_reference.append(result[i])
            else:
                pass
        else:
            papier.entities_from_reference = result

    except Exception as e:
        servicetwocheckout = False
        print("can't process with service two")

    if servicetwocheckout == True:
        print("use of service One")
        processor = Textprocessed("https://arxiv.org/pdf/" + str(papier.doi) + ".pdf")
        text_processed = processor.get_data_from_pdf()
        result = service_one_extraction.ServiceOne(text_processed).get_references()
        if len(papier.entities_from_reference) > 0:
            if len(result) > 0:
                for i in range(len(result)):
                    stop = False
                    j = 0
                    while j < (len(papier.entities_from_reference) - 1):
                        if stop == False:
                            if (
                                result[i].__eq__(papier.entities_from_reference[j])
                                == True
                            ):
                                stop = True
                        j += 1
                    if stop == False:
                        papier.entities_from_reference.append(result[i])

            else:
                pass
        else:
            papier.entities_from_reference = result

    return papier


def remove_file(listedepapier):
    for papier in listedepapier:
        try:
            os.remove(str("knowledgegraph/file/" + papier.doi + ".pdf"))
        except OSError as e:
            print("Error while deleting the file")


if __name__ == "__main__":

    nb_paper_to_request = 17
    block_arxiv_size = 5
    # arxiv_data = Data(nb_paper_to_request).get_set_data()
    # print("nb papiers "+str(len(arxiv_data)))
    papiers = []

    session = session_creator()
    papers = session.query(PapierORM).all()
    arxiv_data = []

    for paper in papers:
        arxiv_data.append(
            Papier(
                paper.title,
                paper.doi,
                convert_dict_to_entities(paper.authors),
                paper.link,
                paper.summary,
                paper.datepublished,
            )
        )

    quotient = nb_paper_to_request / block_arxiv_size

    if quotient > 1:
        length = int(block_arxiv_size * quotient)
        stop = 0
        for i in range(0, length, block_arxiv_size):
            print(i)
            if i + block_arxiv_size < length + 1:
                stop += 5
                temp_papiers = main_function(arxiv_data[i : i + block_arxiv_size])
                for papier in temp_papiers:
                    if len(papier.entities_from_reference) < 15:
                        papier = services_manager(papier)
                papiers += temp_papiers
                remove_file(temp_papiers)

        if nb_paper_to_request - stop > 0:
            temp_papiers = main_function(arxiv_data[stop:nb_paper_to_request])
            for papier in temp_papiers:
                if len(papier.entities_from_reference) < 15:
                    papier = services_manager(papier)
            papiers += temp_papiers
            remove_file(temp_papiers)
    else:
        temp_papiers = main_function(arxiv_data[0:nb_paper_to_request])
        for papier in temp_papiers:
            if len(papier.entities_from_reference) < 15:
                papier = services_manager(papier)
        papiers += temp_papiers
        remove_file(temp_papiers)

    print(len(papiers))
    """
    owl = ontology.Ontology()
    for papier in papiers: 
        owl.add_papier(papier)
    owl.save('result.owl')"""
