import nltk
from operator import itemgetter
from nltk.tag import StanfordNERTagger#, StanfordPOSTagger
import polyglot
from polyglot.text import Text
PATH_TO_JAR='knowledgegraph/nlpmodel/rawnlpmodel/stanford-ner.jar'
PATH_TO_MODEL = 'knowledgegraph/nlpmodel/rawnlpmodel/english.muc.7class.distsim.crf.ser.gz'
stner = StanfordNERTagger(PATH_TO_MODEL,PATH_TO_JAR,encoding='utf-8')
from knowledgegraph.models import Entity


class ServiceOne():

    text_processed = None

    def __init__(self,text):
        self.text_processed = text

    def nltktreelist(self):    
        
        text = self.text_processed    
        persons = [] 

        for l in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text))):
            if isinstance(l,nltk.tree.Tree):
                if l.label() == 'PERSON':
                    if len(l)== 1:
                        if l[0][0] in persons:
                            pass
                        else:
                            persons.append(l[0][0])
                    else:
                        if " ".join(map(itemgetter(0), l)) in persons:
                            pass
                        else:
                            persons.append(" ".join(map(itemgetter(0), l)).strip("*"))

        results = {}
        results['persons']=persons    
        return results


    def get_continuous_chunks(self):
        string = self.text_processed
        continuous_chunk = []
        current_chunk = []

        for token, tag in stner.tag(string.split()):
            if tag != "O":
                current_chunk.append((token, tag))
            else:
                if current_chunk: # if the current chunk is not empty
                    continuous_chunk.append(current_chunk)
                    current_chunk = []
        
        if current_chunk:
            continuous_chunk.append(current_chunk)
        named_entities = continuous_chunk
        named_entities_str = [" ".join([token for token, tag in ne]) for ne in named_entities]
        named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]
        persons = []
        for l in [l.split(",") for l,m in named_entities_str_tag if m == "PERSON"]:
            for m in l:
                for n in m.strip().split(","):
                    if len(n)>0:
                        persons.append(n.strip("*"))
    
        entities={}
        entities['persons']= persons
        
        return entities

    def polyglot_entities(self):
        text = Text(self.text_processed)
        result =[]
        for entity in text.entities:
            etext = " ".join(entity)
            if entity.tag == 'I-PER':
                result.append(etext)            
        return result
    
    def convert_string2entity(self, liste):
        result =[]
        for i in range(len(liste)):
            temp = liste[i].split(" ")
            if len(temp) >2:  # Prend en compte les noms du type David A. Strubbe
                p = Entity()
                p.set_prenom(' '.join(temp[0:-1]))
                p.set_nom(temp[-1])
                result.append(p)
            else:
                if len(temp) >1: # cas normal nom prénom 
                    p = Entity()   
                    p.set_prenom(temp[0])
                    p.set_nom(temp[1])
                    result.append(p)
                else: 
                    p = Entity()   # cas pas normal juste nom ou erreur 
                    p.set_prenom("No firstname")
                    p.set_nom(temp[0])
                    result.append(p)
        return result 

    def get_references(self):
        #nltkresult = self.nltktreelist()["persons"]
        polyglotresult = self.polyglot_entities()
        Standfordresult = self.get_continuous_chunks()["persons"]
        resultList= list(set(polyglotresult) | set(Standfordresult))
        resultList = [x for x in polyglotresult if len(x)>1 ]
        resultList = self.convert_string2entity(resultList)
        forbidden_list = ["Network","Systems","Verification","Research","XVII","Deeep","Dataset","Science","Programming","Mathematical","Analysis","Intelligence","Retrieval","Learning","Machine","Data","Engineering","Update","AGCN","Ct","Measure","Task","Ht","Bert","Momentum","Improved","Random","Are","Towards","Thus","Practical","Online","Systems","Available","Parameter"]
        resultList = [x for x in resultList if x.nom not in forbidden_list]
        return resultList