import textwrap

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from knowledgegraph.controller.data.arxiv import Data
from knowledgegraph.models import Entity


class Awsner:
    def __init__(self, sizechunk):
        self.aws_region = "us-east-1"
        self.sizechunk = int(sizechunk)

    def get_entities(self, text):

        chunks = textwrap.wrap(text, self.sizechunk, break_long_words=False)
        comprehend = boto3.client(
            service_name="comprehend", region_name=self.aws_region
        )
        dict = {}
        compteur_chunk = 0

        for chunk in chunks:

            persons_objects = []
            organisations_objects = []
            date_objects = []
            commercial_objects = []
            event_objects = []
            location_objects = []
            title_objects = []
            chunk_num = str("Chunk_" + str(compteur_chunk))

            try:
                data = comprehend.detect_entities(Text=chunk, LanguageCode="en")
                for entity in data["Entities"]:
                    if entity["Type"] == "PERSON":
                        persons_objects.append(entity["Text"])
                    if entity["Type"] == "ORGANIZATION":
                        organisations_objects.append(entity["Text"])
                    if entity["Type"] == "DATE":
                        date_objects.append(entity["Text"])
                    if entity["Type"] == "COMMERCIAL_ITEM":
                        commercial_objects.append(entity["Text"])
                    if entity["Type"] == "EVENT":
                        event_objects.append(entity["Text"])
                    if entity["Type"] == "LOCATION":
                        location_objects.append(entity["Text"])
                    if entity["Type"] == "TITLE":
                        title_objects.append(entity["Text"])

            except NoCredentialsError:
                print("Unable to locate AWS credentials")
            except ClientError:
                print(
                    "An error occurred (UnrecognizedClientException) \
                when calling the DetectEntities operation: \
                The security AWS token included in the request is invalid"
                )

            information = {}
            information["organisations"] = organisations_objects
            information["date"] = date_objects
            information["commercial"] = commercial_objects
            information["event"] = event_objects
            information["location"] = location_objects
            information["title"] = title_objects
            information["Personne"] = []
            if len(persons_objects) > 0:
                persons_objects = Data(1).process_authors(persons_objects)
                for i in range(len(persons_objects)):
                    information["Personne"].append(persons_objects[i].__dict__)

            dict[chunk_num] = information
            compteur_chunk += 1

        return dict
