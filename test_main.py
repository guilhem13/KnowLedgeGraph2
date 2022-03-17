from knowledgegraph.controller import Pipeline
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
import multiprocessing as mp
from knowledgegraph.owl import ontology
from knowledgegraph.controller import Data

def main_function(block_paper):

    p = Pipeline("https://export.arxiv.org/pdf/",0)
    out_queue = mp.Queue()
    batch_size = 5
    return p.make_traitement_pipeline(block_paper, out_queue, batch_size)

if __name__ == '__main__':

    nb_paper_to_request = 1
    block_arxiv_size = 5
    arxiv_data = Data(nb_paper_to_request).get_set_data()
    print("nb papiers "+str(len(arxiv_data)))

    papiers= []
    quotient= nb_paper_to_request / block_arxiv_size 
    if quotient>1:
        length = int(block_arxiv_size * quotient)
        for i in range(0,length ,block_arxiv_size):
            print(i) 
            papiers+= main_function(arxiv_data[i:i+block_arxiv_size])

        if nb_paper_to_request-(block_arxiv_size*quotient) >0:
            papiers+= main_function(arxiv_data[length :int(length+(nb_paper_to_request - length))])
    else:
        papiers+= main_function(arxiv_data[0:nb_paper_to_request])
    #papiers = main_function()
    print(len(papiers))
    owl = ontology.Ontology()
    for papier in papiers: 
        owl.add_papier(papier)
    owl.save('result.owl')