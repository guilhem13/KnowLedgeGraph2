from owlready2 import get_ontology

a = get_ontology("file://owl/onto3.owl").load()
print(str(a))