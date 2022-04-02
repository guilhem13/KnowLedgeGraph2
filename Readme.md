# Arxiv ontology API 

It's a simple API which can : 
- return entities of an uploading pdf (front)
- return ontology made with 1000 papers in zip format (front)
- manage arxiv database (front)
- Process papers to generate ontology (back)

***

### Features included 

 *  Feature 1 : return entities of an uploading pdf
      * Endpoint : /getner
      * Type : POST
 *  Feature 2 : get ontology made with 1000 papers  
      * Endpoint : /get/ontology
      * Type : GET
 *  Feature 3 : get the size of the database
      * Endpoint : /arxiv/sizebdd
      * Type : Get
 *  Feature 4 : get the size of the database
      * Endpoint : /arxiv/sizebdd
      * Type : Get 

***
## Installation 

Code has been made with Python 3.8.10

Create a virtualenv and activate it:

```shell
python3 -m venv venv
. venv/bin/activate
```
Install Packages 

```shell
pip install -r requirements.txt
```

***
## Run 

In production 

```shell
python3 webapp.py
```
In developement 

```shell
export FLASK_APP=webapp.py
export FLASK_ENV=development
flask run
```
if flask run doesn't work make : 

```shell
python -m flask run
```

