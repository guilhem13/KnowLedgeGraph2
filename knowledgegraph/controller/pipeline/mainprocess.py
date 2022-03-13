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
import glob 
import time 



class Pipeline():

    start=None 

    def __init__(self,arxiv_url,start):
        self.arxiv_url = arxiv_url
        self.start =start
        pass
    """
    def multi_process(self, data, out_queue):
        #if urllib.request.urlopen("http://172.17.0.2:5000/"):
            #print(data.link[0])  
            time.sleep(3)  
            processor = Textprocessed(data.link)            
            text_processed = processor.get_data_from_pdf()
            data.entities_include_in_text = processor.find_entities_in_raw_text()
            #data.entities_from_reference = service_one_extraction.ServiceOne(text_processed).get_references()
            #data.entities_from_reference = service_two_extraction.ServiceTwo(str("file/"+data.doi[0]+".pdf")).get_references()
            #a = service_one_extraction.ServiceOne(text_processed).get_references()
            #a = service_two_extraction.ServiceTwo(str("file/"+data.doi[0]+".pdf")).get_references()
            #b = [ x.__dict__ for x in a ]
            #data.entities_from_reference = b
            data.entities_from_reference = service_one_extraction.ServiceOne(text_processed).get_references()         
            data.url_in_text = processor.find_url_in_text()
            data.doi_in_text = processor.find_doi_in_text()#frfr
            data.date_published = str(data.date_published)
            out_queue.put(data)

    
    def make_traitement_pipeline(self,block_paper,out_queue,batch_size): 
        arxiv_data = block_paper
        res_lst = []        
        f = open("test.json", "a")
        #for i in range(0,len(arxiv_data),batch_size):
        #temp =arxiv_data[i:i+5]
        workers = [ mp.Process(target=self.multi_process, args=(ele, out_queue) ) for ele in block_paper]
            #s = threading.Semaphore(4)
        for work in workers:
              #with s:
            work.start()
        for work in workers: work.join(timeout=5)

            #res_lst = []
        for j in range(len(workers)):
            res_lst.append(out_queue.get())
        #f.write(json.dumps(out_queue.get().__dict__))    

        for test in res_lst: 
           f.write(json.dumps(test.__dict__,default=lambda x: x.__dict__))
        f.close()
        return res_lst
     # TODO récolter le nombre de coeur pour ensuite le mettre sur le code
     # gérer le problème quand c'est 10000  
     #https://blog.ruanbekker.com/blog/2019/02/19/parallel-processing-with-python-and-multiprocessing-using-queue/
     #https://towardsdatascience.com/pool-limited-queue-processing-in-python-2d02555b57dc
###########################################################################################################"""

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
            #data.entities_from_reference = service_one_extraction.ServiceOne(text_processed).get_references() 
            print("taille du texte ")
            print(len(data.entities_from_reference))
            #print(len(text_processed))"""
            #data.entities_from_reference = processor.find_entites_based_on_regex(text_processed)
            entities_from_regex = processor.find_entites_based_on_regex(text_processed)
            """entities_from_serviceone = service_one_extraction.ServiceOne(text_processed).get_references()
            final_entities_list =[]
            print(len(entities_from_regex))
            print(len(entities_from_serviceone))
            if len(entities_from_regex) >0 :
                if len(entities_from_serviceone)>0:
                    for i in range(len(entities_from_serviceone)): 
                        j = 0
                        stop = False 
                        while (j < len(entities_from_regex)):# or (stop == False):
                            if entities_from_serviceone[i].__eq__(entities_from_regex[j])==True:
                                final_entities_list.append(entities_from_regex[j])
                                stop = True
                            j = j+1
                        
                        final_entities_list.append(entities_from_serviceone[i])

                    data.entities_from_reference =  final_entities_list
                else:
                    data.entities_from_reference =  entities_from_regex
            else: 
                data.entities_from_reference =  entities_from_serviceone """
            data.entities_from_reference = entities_from_regex #final_entities_list
            data.url_in_text = processor.find_url_in_text()
            data.doi_in_text = processor.find_doi_in_text()#frfr
            data.date_published = str(data.date_published) # TODO a enlever c'était pour le test de json
            #before  data.link[0] #TODO dans le cas où l'on est dans le service 2
            #os.remove(str("knowledge/file/"+data.doi+".pdf")) 
            out_queue.put(data)

    
    def make_traitement_pipeline(self,block_paper,out_queue,batch_size): 
        arxiv_data = block_paper
        res_lst = []        
        f = open("test2.json", "a")
        #for i in range(0,len(arxiv_data),1):
        #    temp =arxiv_data[i:i+5]
        workers = [ mp.Process(target=self.multi_process, args=(ele, out_queue) ) for ele in block_paper]
                #s = threading.Semaphore(4)
        for work in workers:
                #with s:
            work.start()
        for work in workers: work.join(timeout=3)

                #res_lst = []
        for j in range(len(workers)):
            res_lst.append(out_queue.get())
        
        
        files = glob.glob('knowledgegraph/file/*.pdf', recursive=True)
        for fh in files:
            try:
                os.remove(fh)
            except OSError as e:
                print("Error: %s : %s" % (fh, e.strerror))

        for test in res_lst: 
           f.write(json.dumps(test.__dict__,default=lambda x: x.__dict__))
        f.close()
        return res_lst
     # TODO récolter le nombre de coeur pour ensuite le mettre sur le code
     # gérer le problème quand c'est 10000  
     


    

    