import nltk
from operator import itemgetter
from nltk.tag import StanfordNERTagger#, StanfordPOSTagger
PATH_TO_JAR='nlpmodel/rawnlpmodel/stanford-ner.jar'
PATH_TO_MODEL = 'nlpmodel/rawnlpmodel/english.muc.7class.distsim.crf.ser.gz'
stner = StanfordNERTagger(PATH_TO_MODEL,PATH_TO_JAR,encoding='utf-8')
from models import Entity


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
    
    def convert_string2entity(self, liste):
        result =[]
        for i in range(len(liste)):
            temp = liste[i].split(" ")
            if len(temp) >2:  # Prend en compte les noms du type David A. Strubbe
                p = Entity()
                p.set_prenom(str(temp[0]+" "+temp[1]))
                p.set_nom(temp[2])
                result.append(p)
            else:
                if len(temp) >1:
                    p = Entity()
                    p.set_prenom(temp[0])
                    p.set_nom(temp[1])
                    result.append(p)
                else:  
                    p = Entity()
                    p.set_prenom("pas_de_prenom") #TODO gérer cette erreur 
                    p.set_nom(temp[0])
                    result.append(p) #TODO parfois le retour n'est pas prenom nom il faut donc gérer ce porblème 
        return result 

    def get_references(self):
        nltkresult = self.nltktreelist()["persons"]
        Standfordresult = self.get_continuous_chunks()["persons"]
        resultList= list(set(nltkresult) | set(Standfordresult))
        resultList = [x for x in nltkresult if len(x)>1 ]
        resultList = self.convert_string2entity(resultList)
        return resultList