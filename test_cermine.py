import glob
from importlib.metadata import FileHash 
from knowledgegraph.nlpmodel import service_two_extraction
import requests
import time

headers = {'Content-Type': 'application/binary'}
data = open('knowledgegraph/file/2203.09510v1.pdf', 'rb').read()
response = requests.post('http://cermine.ceon.pl/extract.do', headers=headers, data=data)
 
files = glob.glob('knowledgegraph/file/*.pdf', recursive=True)
for fh in files:
    print(fh)
    time.sleep(1)
    headers = {'Content-Type': 'application/binary'}
    data = open(fh, 'rb').read()
    response = requests.post('http://cermine.ceon.pl/extract.do', headers=headers, data=data)
    print(len(response.content))
    print("done")