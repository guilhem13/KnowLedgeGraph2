from logging import exception
from hdfs.ext.kerberos import KerberosClient

folder_hdfs = "/education/cs_2022_spring_1/g.maillebuau-cs/project"
csv_localisation = "ProjetPyhtonAPI/hadoop/metadata_database.csv"#"/home/guigui/Documents/ProjetPyhtonAPI/hadoop/metadata_database.csv"


try:
    client = KerberosClient("http://hdfs-nn-1.au.adaltas.cloud:50070")
except exception as e:
    print("Error while connecting to hdfs ")
    print(e)

try:
    client.upload(folder_hdfs, csv_localisation)
except exception as e:
    print("Can't export database")
    print(e)
