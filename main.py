import nltk
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("words")
import ast
import multiprocessing as mp
import os
import json 
import sys
import getopt
import requests
from pathlib import Path
from knowledgegraph.controller.treatment.mainprocess import Pipeline
from bdd.manager_bdd import session_creator
from bdd.paper_model_orm import PapierORM
from knowledgegraph.controller.treatment.processingpipeline import Textprocessed
from knowledgegraph.models import Entity, Papier
from knowledgegraph.nlpmodel import (service_one_extraction,
                                     service_two_extraction)
from knowledgegraph.owl import ontology


def main_args(argv):
   nbpapier = ''
   outputfile = Path("./")
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["help","nbpapier=","ofile="])
   except getopt.GetoptError:
      print('main.py -i <nbpapier> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('main.py -i <nbpapier> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--nbpapier"):
         nbpapier = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print('nbpapier is '+nbpapier)
   print('Output file is '+outputfile)
   return nbpapier,outputfile

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
        p.set_prenom(item["prenom"].strip())
        p.set_nom(item["nom"].strip())
        p.set_name(item["nom"] + item["prenom"])
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

    if servicetwocheckout == False:
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


def remove_file(papier):
        try:
            os.remove(str("knowledgegraph/file/" + papier.doi + ".pdf"))
        except OSError as e:
            print("Error while deleting the file")

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

def client_api_ner(papiers): 
    links = [x.link for x in papiers]
    json_data={}
    for i in range(len(links)):
        json_data[i] =links[i]
    headers = {'content-type': 'application/json'}

    r = requests.post(url = "http://localhost:6000/get/entities", data =json.dumps(json_data), headers =headers)

    reponse =  ast.literal_eval(r.text)
    for item in reponse: 
        papier_json = json.loads(item)
        for papier in papiers:
            if papier.link == papier_json['link']:
                papier.doi_in_text =papier_json['doi_in_text']
                papier.url_in_text = papier_json['url_in_text']
                papier.entities_include_in_text = papier_json['entities_include_in_text']
                papier.entities_from_reference = convert_json_to_entities(papier_json['entities_from_reference'])
    
    return papiers



if __name__ == "__main__":
    
    #nb_paper_to_request, filename = main_args(sys.argv[1:])
    #nb_paper_to_request = 5 
    nb_paper_to_request = 5#int(nb_paper_to_request)
    block_arxiv_size = 5
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
    owl = ontology.Ontology()

    if quotient > 1:
        length = int(block_arxiv_size * quotient)
        stop = 0
        for i in range(0, length, block_arxiv_size):
            print(i)
            if i + block_arxiv_size < length + 1:
                stop += 5
                temp_papiers = client_api_ner(arxiv_data[i : i + block_arxiv_size])
                #temp_papiers = main_function(arxiv_data[i : i + block_arxiv_size])
                for papier in temp_papiers:
                    if len(papier.entities_from_reference) < 15:
                        response = requests.post(papier.link+".pdf")
                        with open("knowledgegraph/file/"+papier.doi+".pdf", 'wb') as f:
                            f.write(response.content)
                        papier = services_manager(papier)
                        remove_file(papier)

                for papier in papiers: 
                    owl.add_papier(papier)
                owl.save('knowledgegraph/owl/onto10.owl')
                papiers += temp_papiers

        if nb_paper_to_request - stop > 0:
            temp_papiers = main_function(arxiv_data[stop:nb_paper_to_request])
            for papier in temp_papiers:
                if len(papier.entities_from_reference) < 15:
                    response = requests.post(papier.link+".pdf")
                    with open("knowledgegraph/file/"+papier.doi+".pdf", 'wb') as f:
                        f.write(response.content)
                    papier = services_manager(papier)
                    remove_file(papier)
            papiers += temp_papiers
    else:
        temp_papiers = main_function(arxiv_data[0:nb_paper_to_request])
        for papier in temp_papiers:
            if len(papier.entities_from_reference) < 15:
                response = requests.post(papier.link+".pdf")
                with open("knowledgegraph/file/"+papier.doi+".pdf", 'wb') as f:
                    f.write(response.content)
                papier = services_manager(papier)
                remove_file(papier)
        papiers += temp_papiers
    print(len(papiers))

    """
    owl = ontology.Ontology()
    for papier in papiers: 
        owl.add_papier(papier)
    owl.save('result.owl')"""
