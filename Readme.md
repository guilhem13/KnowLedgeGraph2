# Extract text from pdf 

It's a simple REST API which parses pdf files in order to extract text from it.
The text file are stocked in a database

***

### Features included 

 *  Feature 1 :  Upload pdf. Save its data into a database and return Id 's document
      * Endpoint : /documents
      * Type : POST
 *  Feature 2 : Get the metadata of an uploading file by its id  
      * Endpoint : /documents/{id}
      * Type : GET
 *  Feature 3 : Request the text of files uploaded by id
      * Endpoint : /text/{id}.txt
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

