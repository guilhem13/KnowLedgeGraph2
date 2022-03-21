"""from threading import local
from bdd.paper_model_orm import PapierORM
from bdd.manager_bdd import session_creator
from knowledgegraph.models import Papier , Entity
from knowledgegraph.controller import Data
import ast
import glob , os 
import polyglot
from polyglot.text import Text
from knowledgegraph.controller.pipeline.processingpipeline import Textprocessed
import re 

a ="[1] K. J. Astrom and B. M. Appendices Bernhardsson, Comparison of riemann and lebesgue sampling for first order stochastic systems, in Proceedings of the 41st IEEE Conference on Decision and Control, 2002., vol. 2, pp. 20112016, IEEE, 2002.  [2] P. Tabuada, Event-triggered real-time scheduling of stabilizing control tasks, IEEE Transactions on Automatic Control, vol. 52, no. 9, pp. 16801685, 2007.  [3] A. S. Kolarijani and M. Mazo, Formal traffic characterization of lti event-triggered control systems, IEEE Transactions on Control of Network Systems, vol. 5, no. 1, pp. 274283, 2016.  [4] P. Tabuada, Verification and control of hybrid systems: a symbolic  approach. Springer Science & Business Media, 2009.  [5] G. d. A. Gleizer and M. Mazo Jr, Scalable traffic models for scheduling of linear periodic event-triggered controllers, IFAC-PapersOnLine, vol. 53, no. 2, pp. 27262732, 2020.  [6] G. d. A. Gleizer and M. Mazo, Towards traffic bisimulation of linear periodic event-triggered controllers, IEEE Control Systems Letters, vol. 5, no. 1, pp. 2530, 2020.  [7] G. de A. Gleizer and M. Mazo Jr, Computing the sampling performance of event-triggered control, in Proceedings of the 24th International Conference on Hybrid Systems: Computation and Control, pp. 17, 2021.  [8] G. Delimpaltadakis, G. de Albuquerque Gleizer, I. van Straalen, and M. Mazo Jr., Etcetera: beyond event-triggered control, in Proceedings of the 25th International Conference on Hybrid Systems: Computation and Control, 2022.  [9] M. Cubuktepe, N. Jansen, S. Junges, J.-P. Katoen, and U. Topcu, Scenario-based verification of uncertain mdps, in International Conference on Tools and Algorithms for the Construction and Analysis of Systems, pp. 287305, Springer, 2020.  [10] T. S. Badings, A. Abate, N. Jansen, D. Parker, H. A. Poonawala, and M. Stoelinga, Sampling-based robust control of autonomous systems with non-gaussian noise, arXiv preprint arXiv:2110.12662, 2021. [11] M. Campi and S. Garatti, The exact feasibility of randomized solutions of uncertain convex programs, SIAM Journal on Optimization, vol. 19, no. 3, pp. 12111230, 2008.  [12] M. C. Campi, S. Garatti, and F. A. Ramponi, A general scenario theory for nonconvex optimization and decision making, IEEE Transactions on Automatic Control, vol. 63, no. 12, pp. 40674078, 2018. [13] S. Garatti and M. C. Campi, Risk and complexity in scenario  optimization, Mathematical Programming, pp. 137, 2019.  [14] M. C. Campi and S. Garatti, Scenario optimization with relaxation: a new tool for design and application to machine learning problems, in 2020 59th IEEE Conference on Decision and Control (CDC), pp. 24632468, IEEE, 2020.  [15] W. H. Heemels, M. Donkers, and A. R. Teel, Periodic event-triggered control for linear systems, IEEE Transactions on automatic control, vol. 58, no. 4, pp. 847861, 2012.  [16] G. de Albuquerque Gleizer and M. Mazo Jr, Chaos and order in  event-triggered control, arXiv e-prints, 2022.  [17] K. Chatterjee, L. Doyen, and T. A. Henzinger, Quantitative languages, ACM Transactions on Computational Logic (TOCL), vol. 11, no. 4, pp. 138, 2010.  [18] R. M. Karp, A characterization of the minimum cycle mean in a  digraph, Discrete mathematics, vol. 23, no. 3, pp. 309311, 1978.  [19] J. Weston and C. Watkins, Multi-class support vector machines, tech.  rep., Citeseer, 1998.  [20] M. Mazo, A. Anta, and P. Tabuada, On self-triggered control for linear systems: Guarantees and complexity, in 2009 European Control Conference (ECC), pp. 37673772, IEEE, 2009.  [21] C.-W. Hsu and C.-J. Lin, A comparison of methods for multiclass support vector machines, IEEE transactions on Neural Networks, vol. 13, no. 2, pp. 415425, 2002.  [22] K. Crammer and Y. Singer, On the algorithmic implementation of multiclass kernel-based vector machines, Journal of machine learning research, vol. 2, no. Dec, pp. 265292, 2001.  \x0c"
forbidden_part =['Appendices','Supplementary Material','Supplementary material']
#print(Text(a).entities)

res = [a[40:].find(ele) for ele in forbidden_part 

processor = Textprocessed("https://arxiv.org/pdf/2203.09382v1.pdf") #before  data.link[0]        
text_processed = processor.get_data_from_pdf()
#print(text_processed)

res = processor.find_entites_based_on_regex(text_processed)
print(len(res))

def find_regex_style(regexstyle, text):        
  regexp = re.compile(regexstyle)
  return regexp.findall(text)

def check_doublon (listcorrect, listaverifier):
  for i in range(len(listaverifier)): 
    for j in range(len(listcorrect)): 
      if listaverifier[i] in listcorrect[j]:
        listaverifier[i] = "TOREMOVE"
  listaverifier = [x for x in listaverifier if x != "TOREMOVE"]
  return listaverifier

def get_sec_format(text): #APA style , 
  result=[] 
  template_one = find_regex_style("[A-Z][a-z]+,\s[A-Z]\.[A-Z]\.[A-Z]\.",text) #Johnson, D. D. P.
  template_two= find_regex_style("[A-Z][a-z]+,\s[A-Z]\.[A-Z]\.",text) #Johnson, D. D.
  template_three= find_regex_style("[A-Z][a-z]+,\s[A-Z]\.",text) #Johnson, D.

  #print(text)
  print(len(template_one))
  print(len(template_three))
  print(template_two)

  if len(template_one)>0:
    result += template_one
  if len(template_two)>0:
    if len(result)>0:
      template_two = check_doublon(result,  template_two)
      template_two = list(set(template_two))
      result = result + template_two
    else: 
      result+=template_two
  if len(template_three)>0:
    if len(result)>0:
       template_three = check_doublon(result,  template_three)
       template_three = list(set(template_three))
       result = result + template_three
    else: 
       result+=template_three
      
  return result

print(get_sec_format(text_processed))

session = session_creator()
# User is the name of table that has a column name
papers = session.query(PapierORM).filter().limit(5).all()
print(len(papers))


def convert_dict_to_entities(stringdict):
    entities_list = []
    res = ast.literal_eval(stringdict)
    for item in res: 
        p = Entity()   
        p.set_prenom(item['prenom'])
        p.set_nom(item['nom'])
        entities_list.append(p)

    return entities_list

papers = session.query(PapierORM).all()
paper_list = []
for paper in papers :
    paper_list.append(Papier(paper.title,paper.doi,convert_dict_to_entities(paper.authors),paper.link,paper.summary,paper.data_published))


p = Entity()   
p.set_prenom('prenom')
p.set_nom('nom')

a = Entity()   
a.set_prenom('prenom')
a.set_nom('nom')


files = glob.glob('knowledgegraph/file/*.pdf', recursive=True)

for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

from refextract import extract_references_from_file
references = extract_references_from_file('1810.04805.pdf')
listreferences = []
print(references)
for item in references:
    result =""
    if 'raw_ref' in item.keys(): 
        result.append(item['raw_ref'])
    if 'year' in item.keys():
        result += "&!&"
        result.append
    listreferences.append(item['raw_ref']) 

print(listreferences)
files = glob.glob('knowledgegraph/file/*.pdf', recursive=True)
for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

dict ={}

persons_objects =[]
organisations_objects =['azeaaedaaeded','adedafdeda','afefefedcfdc']
lists = ['persons_objects','organisations_objects']
output = {}
data = {listname: locals()[listname] for listname in lists}


p = Entity()   
p.set_prenom('prenom1')
p.set_nom('nom1')

a = Entity()   
a.set_prenom('prenom1')
a.set_nom('nom1')


vv = []
vv.append(p)
vv.append(a)

data['Personne'] = []
for i in range(len(vv)): 
    data['Personne'].append(vv[i].__dict__)

dict['chunk_1']=data
print(dict)

with open('abc.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

"""
import glob 
import os 
files = glob.glob('knowledgegraph/file/*.pdf', recursive=True)

for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))