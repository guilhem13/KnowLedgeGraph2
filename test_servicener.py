from typing import Type
import requests
import json 



json_data = {
    'papier_1':'http://arxiv.org/pdf/2203.06419v1',
    'papier_2':'http://arxiv.org/pdf/2203.06416v1',
    'papier_3':'http://arxiv.org/pdf/2203.07372v1'
}

import ast 
headers = {'content-type': 'application/json'}
r = requests.post(url = "http://localhost:6000/get/entities", data =json.dumps(json_data), headers =headers)

print(type(r.text))
a = ast.literal_eval(r.text)
print(type(a))
print(len(a))
for item in a : 
    b = json.loads(item)
    print(b['link'])

"""
for item in json.loads(r.text)[0]: 
    print(item['link'])"""