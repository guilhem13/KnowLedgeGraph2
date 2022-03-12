import unicodedata
import re 
from .pdfx import PDFx
from .undesirable_char import undesirable_char_replacements 
from knowledgegraph.controller import Data
from knowledgegraph.models import Entity
from refextract import extract_references_from_file

class Textprocessed(): 
    url = None
    raw_text =None

    def __init__(self,url):
        self.url =url

    def get_references_part(self,Pdf_Readed):
        
        for bad_char, replacement in undesirable_char_replacements.items():
            Pdf_Readed = Pdf_Readed.replace(bad_char, replacement)
        result=""
        try:
            temp = unicodedata.normalize('NFKD',Pdf_Readed).encode('ascii','ignore').decode('unicode_escape').encode('ascii','ignore').decode()
        except: 
            temp = Pdf_Readed

        #TODO inclure 
        """[u'references',u'r\u00C9f\u00E9rences',u'r\u00C9f\u00C9rences',u'r\xb4ef\xb4erences',u'bibliography',u'bibliographie',u'literaturverzeichnis',u'citations',u'refs',u'publications',u'r\u00E9fs',u'r\u00C9fs',u'reference',u'r\u00E9f\u00E9rence',u'r\u00C9f\u00C9rence']"""
        
        keyword_list = ['\nReferences\n', '\nREFERENCES\n','\nreferences\n','REFERENCES','References\n','References'] #TODO voir les cas où c'est juste " Reference " exeple => https://arxiv.org/pdf/2202.03954v1.pdf
        keyword = [ele for ele in keyword_list if(ele in temp)]
        if keyword != None:
            if len(keyword) == 1: 
                keyword = str(keyword[0]) 
                index = temp.index(keyword) # check ici parcequ'il y a plusieurs versions de références 
                result = temp[index +len(keyword):]
                return result
            else:
                if(len(keyword)!=0):
                    index_keyword = [temp.index(ele) for ele in keyword]
                    delta = max(index_keyword)-min(index_keyword)
                    if delta < 14: 
                        keyword = str(keyword[0]) 
                        index = temp.index(keyword) # check ici parcequ'il y a plusieurs versions de références 
                        result = temp[index +len(keyword):]
                        return result
                    else: 
                        return "erreur problème: Plusieurs références ! "  #TODO enlever cette partie non disruptive 
                else:
                    if temp.count("Reference") == 1: 
                        index = temp.index("Reference") # check ici parcequ'il y a plusieurs versions de références 
                        result = temp[index +len(keyword):]
                        return result
                    else: 
                        return "erreur problème: Plusieurs références ! 2" 

    def get_references_part2(filename): 
        references = extract_references_from_file(filename)
        return references

    def clean_references_part(self,data):
        temp = re.sub(' +', ' ', data)
        temp = temp.replace("-\n", "") # reconstruire les retours à la ligne 
        temp = temp.replace("\n"," ") #rajout d'espace 
        return temp

    def find_entities_in_raw_text(self):
        
        named_re = re.compile("(?:\(|\[)((?:[ a-zA-Z\.,\n-]+(?:\(|\[)*(?:19|20)[0-9]{2}(?:\)|\])*[; \n]*)+)(?:\)|\])")
        result = named_re.findall(self.raw_text)
        return result

    def find_regex_style(self,regexstyle, text):        
        regexp = re.compile(regexstyle)
        return regexp.findall(text)
    
    def check_doublon (self,listcorrect, listaverifier):
        result = listaverifier
        for item in listaverifier: 
            for item2 in listcorrect: 
                if item in item2:
                    if "Astrom" in item:
                        print("$$db$$") 
                        print(item)
                        print(item2)
                    result.remove(item)
        #print(result)
        return result


    
    def find_entites_based_on_regex(self,text):        
        Entitylist = []

        fithformat = self.find_regex_style('[A-Z][a-z]+\s[a-zA-Z]\.\s[a-zA-Z]\.\s[a-zA-Z]+[,.]',text) #James J. H. Little,
        fithformat2 = self.find_regex_style('[A-Z][a-z]+\s[a-zA-Z]\.\s[a-zA-Z]\.\s[a-zA-Z]+\sand',text) #James J. H. Little and
        fithformat = [x[:-1] for x in fithformat] if len(fithformat)>0 else []
        fithformat2 = [x[:-4] for x in fithformat2] if len(fithformat2)>0 else []
        Style_one = fithformat +fithformat2
        Style_one = list(set(Style_one))

        fourformat = self.find_regex_style('[A-Z][a-z]+\s[a-zA-Z]\.\s[a-zA-Z]+[,.]',text) #James J. Little,
        fourformat2 = self.find_regex_style('[A-Z][a-z]+\s[a-zA-Z]\.\s[a-zA-Z]+\sand',text) #James J. Little and
        fourformat = [x[:-1] for x in fourformat] if len(fourformat)>0 else []
        fourformat2 = [x[:-4] for x in fourformat2] if len(fourformat2)>0 else []
        Style_two = fourformat + fourformat2
        Style_two = list(set(Style_two))

        thirdformat = self.find_regex_style("[A-Z]\. [A-Z]\.\s[A-Z]\.\s[a-zA-Z]+[,.]",text) #J. F. P. Kooijffrr
        thirdformat2 = self.find_regex_style("[A-Z]\. [A-Z]\.\s[A-Z]\.\s[a-zA-Z]+\sand",text) #J. F. P. Kooijffrr and
        thirdformat = [x[:-1] for x in thirdformat] if len(thirdformat)>0 else []
        thirdformat2 = [x[:-4] for x in thirdformat2] if len(thirdformat2)>0 else []
        Style_three = thirdformat + thirdformat2
        Style_three = list(set(Style_three))

        """Style_two = self.check_doublon(Style_one, Style_two)
        result = Style_one + Style_two 
        Style_three = self.check_doublon(result, Style_three)
        result = result + Style_three """
        result = Style_one + Style_two + Style_three
        result = list(set(result))

        firstformat = self.find_regex_style("[A-Z]\. [a-zA-Z]+[,.]",text) # E. Behjat
        firstformat2 = self.find_regex_style("[A-Z]\. [a-zA-Z]+\sand",text) # E. Behjat and
        firstformat = [x[:-1] for x in firstformat] if len(firstformat)>0 else []
        firstformat2 = [x[:-4] for x in firstformat2] if len(firstformat2)>0 else []
        firstformat = firstformat + firstformat2 
        firstformat = list(set(firstformat))

        secondformat = self.find_regex_style("[A-Z]\.\s+[A-Z]\. [a-zA-Z]+[,.]",text) #  B. K. Jang 
        secondformat2 = self.find_regex_style("[A-Z]\.\s+[A-Z]\. [a-zA-Z]+\sand",text)# B. K. Jang  and
        secondformat2 = [x[:-4] for x in secondformat2] if len(secondformat2)>0 else []
        secondformat = [x[:-1] for x in secondformat] if len(secondformat)>0 else []
        secondformat = secondformat + secondformat2
        secondformat = list(set(secondformat))

        if len(firstformat) >0:
            if len(result) >0: 
                print(firstformat)
                firstformat = self.check_doublon(result, firstformat)
            firstformat = list(set(firstformat))
            result = result + firstformat
        if len(secondformat) >0:  
            if len(result) >0:     
                secondformat = self.check_doublon(result, secondformat)
            secondformat = list(set(secondformat))
            result = result + secondformat
        """
        sithformat = self.find_regex_style(r"[A-Z]\.\s[a-zA-Z]+\sand\s[A-Z]\. [a-zA-Z]",text) #F. Englert and R. Brout, captuer le F.Englert
        if len(sithformat) >0:
            sithformat = [x.split(" and")[0] for x in sithformat ]
            if len(result) >0: 
                sithformat = self.check_doublon (result, sithformat)
            sithformat = list(set(sithformat))
            result = result + sithformat"""

        sevenformat = self.find_regex_style(r"[A-Z][a-z]+\s[A-Z][a-z]+,\s[A-Z][a-z]+\s[A-Z][a-z]+,\sand\s[A-Z][a-z]+\s[A-Z][a-z]+",text) #Alan Akbik, Duncan Blythe, and Roland Vollgraf
        if len(sevenformat) >0:
            newsevenformat =[]
            for item in sevenformat:
                temp = item.split(", ")
                newsevenformat.append(temp[0])
                newsevenformat.append(temp[1])
                newsevenformat.append(temp[2][4:])
            if len(result) >0: 
                newsevenformat = self.check_doublon (result, newsevenformat)
            newsevenformat = list(set(newsevenformat))
            result = result + newsevenformat

        if len(result) > 0:
            regex_remove = re.compile('^[A-Z]\. [A-Z]\.$')
            regex_remove2 = re.compile('^[A-Z]\. [A-Z]$')
            result = [x for x in result if regex_remove.match(x) == None]# remove "A. R "  part 
            result = [x for x in result if regex_remove2.match(x) == None]
            #result = [x[:-1] for x in result ]   
            result = Data(1).process_authors(result)
            Entitylist.extend(result)
        else : 
            #print("liste nulle")
            pass
        
             
        if len(Entitylist) ==0:
            p = Entity()
            p.set_prenom("guilhem")
            p.set_nom("maillebuau")
            Entitylist.append(p)
              
        return Entitylist    
                    


    
    def find_url_in_text(self):

        arxiv_regex = r"""arxiv:\s?([^\s,]+)"""
        arxiv_regex2 = r"""arxiv.org/abs/([^\s,]+)"""
        url_regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""  # noqa: E501
        res = re.findall(arxiv_regex , self.raw_text, re.IGNORECASE) + re.findall(arxiv_regex2, self.raw_text, re.IGNORECASE) + re.findall(url_regex, self.raw_text, re.IGNORECASE)
        return list(dict.fromkeys([r.strip(".") for r in res]))
    
    def find_doi_in_text(self):

        doi_regex = r"""DOI:\s?([^\s,]+)"""
        res = set(re.findall(doi_regex, self.raw_text, re.IGNORECASE))
        return list(dict.fromkeys([r.strip(".") for r in res]))


    def get_data_from_pdf(self):

        pdf = PDFx(self.url)
        textfrompdf = pdf.get_text()
        self.raw_text = textfrompdf
        textfrompdf = self.clean_references_part(self.get_references_part(textfrompdf))
        return textfrompdf
    
    def get_data_from_file(self,file_localisation):
        pdf = PDFx(file_localisation)
        textfrompdf = pdf.get_text()
        textfrompdf = self.clean_references_part(self.get_references_part(textfrompdf))
        return textfrompdf

    def __getattr__(self):
        return self.raw_text
        
    