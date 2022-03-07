from pickle import TRUE
from unittest import result
from knowledgegraph.controller import Data , Textprocessed
from knowledgegraph.nlpmodel import service_one_extraction, service_two_extraction
from multiprocessing.pool import ThreadPool as Pool #TODO A enlever 
import json
from multiprocessing import Process
import multiprocessing as mp
import urllib.request
import threading
from multiprocessing import cpu_count
import os
import time 



class Pipeline():

    start=None 

    def __init__(self,arxiv_url,start):
        self.arxiv_url = arxiv_url
        self.start =start
        pass

###########################################################################################################

    def multi_process(self, data, out_queue):
        #if urllib.request.urlopen("http://172.17.0.2:5000/"):
            #print(data.link[0])  
            time.sleep(3)  
            processor = Textprocessed(data.link) #before  data.link[0]        
            text_processed = processor.get_data_from_pdf()
            data.entities_include_in_text = processor.find_entities_in_raw_text()
            """try: 
                 data.entities_from_reference = service_two_extraction.ServiceTwo(str("file/"+data.doi[0]+".pdf")).get_references()
            except Exception as e:
                print("Service two didn't work ")
                print(e)
                data.entities_from_reference =service_one_extraction.ServiceOne(text_processed).get_references() """
            #data.entities_from_reference = service_one_extraction.ServiceOne(text_processed).get_references()
            #data.entities_from_reference = service_two_extraction.ServiceTwo(str("file/"+data.doi[0]+".pdf")).get_references()
            #a = service_one_extraction.ServiceOne(text_processed).get_references()
            #a = service_two_extraction.ServiceTwo(str("file/"+data.doi[0]+".pdf")).get_references()
            #b = [ x.__dict__ for x in a ]
            #data.entities_from_reference = b
            data.entities_from_reference = service_one_extraction.ServiceOne(text_processed).get_references()         
            data.url_in_text = processor.find_url_in_text()
            data.doi_in_text = processor.find_doi_in_text()#frfr
            os.remove(str("file/"+data.doi+".pdf"))#before  data.link[0]
            out_queue.put(data)

    
    def make_traitement_pipeline(self,block_paper,out_queue,batch_size): 
        arxiv_data = block_paper
        res_lst = []        
        #f = open("test.json", "a")
        for i in range(0,len(arxiv_data),batch_size):
            temp =arxiv_data[i:i+5]
            workers = [ mp.Process(target=self.multi_process, args=(ele, out_queue) ) for ele in temp]
            #s = threading.Semaphore(4)
            for work in workers:
                #with s:
                work.start()
            for work in workers: work.join(timeout=5)

            #res_lst = []
            for j in range(len(workers)):
                res_lst.append(out_queue.get())
                #f.write(json.dumps(out_queue.get().__dict__))

        #for test in res_lst: 
        #   f.write(json.dumps(test.__dict__))
        #f.close()
        return res_lst
     # TODO récolter le nombre de coeur pour ensuite le mettre sur le code
     # gérer le problème quand c'est 10000  


    

    