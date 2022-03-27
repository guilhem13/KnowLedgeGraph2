import csv
import sys 
sys.path.append("./")
from bdd.manager_bdd import session_creator
from bdd.paper_model_orm import PapierORM

session = session_creator()

def clean_string(rowinformation):
    char_to_replace = {
        "\n": " ",
        ",": ";",
    }
    for key, value in char_to_replace.items():
        rowinformation = rowinformation.replace(key, value)
    return rowinformation


f = open("hadoop/metadata_database2.csv", "w")
out = csv.writer(f)
out.writerow(["doi", "title", "authors", "link", "summary", "date_published"])

for item in session.query(PapierORM).all():
    out.writerow(
        [
            item.doi,
            clean_string(item.title),
            clean_string(item.authors),
            item.link,
            clean_string(item.summary),
            clean_string(item.datepublished),
        ]
    )
f.close()
