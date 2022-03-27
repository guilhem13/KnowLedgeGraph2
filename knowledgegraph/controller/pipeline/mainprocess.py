import glob
import json
import multiprocessing as mp
import os
import threading
import time
import urllib.request
from multiprocessing import Process, cpu_count
from multiprocessing.pool import ThreadPool as Pool  # TODO A enlever
from pickle import TRUE
from unittest import result

import requests

import test_cermine
from knowledgegraph.controller import Data, Textprocessed
from knowledgegraph.nlpmodel import (service_one_extraction,
                                     service_two_extraction)


class Pipeline:

    start = None

    def __init__(self, arxiv_url, start):
        self.arxiv_url = arxiv_url
        self.start = start
        pass

    ###########################################################################################################"""

    def multi_process(self, data, out_queue):
        time.sleep(3)
        processor = Textprocessed(data.link)
        print(data.link)
        text_processed = processor.get_data_from_pdf()
        data.entities_include_in_text = processor.find_entities_in_raw_text()
        entities_from_regex = processor.find_entites_based_on_regex(text_processed)
        data.entities_from_reference = entities_from_regex 
        data.url_in_text = processor.find_url_in_text()
        data.doi_in_text = processor.find_doi_in_text()
        data.datepublished = str(data.datepublished)
        out_queue.put(data)

    def make_traitement_pipeline(self, block_paper, out_queue, batch_size):
        arxiv_data = block_paper
        res_lst = []
        #f = open("test2.json", "a")
        workers = [
            mp.Process(target=self.multi_process, args=(ele, out_queue))
            for ele in block_paper
        ]
        # s = threading.Semaphore(4)
        for work in workers:
            # with s:
            work.start()
        for work in workers:
            work.join(timeout=3)

        # res_lst = []
        for j in range(len(workers)):
            res_lst.append(out_queue.get())

        """for test in res_lst:
            f.write(json.dumps(test.__dict__, default=lambda x: x.__dict__))
        f.close()"""
        return res_lst

