# Arxiv ontology API 

It's a simple API which can : 
- return entities of an uploading pdf thanks to AWS comprehend Service(front)
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
      * Type : GET
 *  Feature 4 : get the size of the database
      * Endpoint : /arxiv/sizebdd
      * Type : GET 

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
***
## Run with docker

### Installation

```shell
docker build -t projetpythonapi .
```
### Installation

```shell
docker run -d -p 5000:5000 projetpythonapi
```

***
## Usage
***

## Entrypoint /getner 

You have to add you AWS security token. For that: 
- Be sure to start your Lab
- Create a folder in your computer  => ~/.aws/ 
- Add a credentials file inside this folder 
- Then you have  ~/.aws/credentials
- Inside this credentials file add the content of the Cloud Access AWS with vi or vim

The cloud access aws looks like that : 

```shell
[default]
aws_access_key_id=********
aws_secret_access_key=********
aws_session_token=**********
```
Once that, you can use this entrypoint 

You can watch the documentation with => http://localhost:5000/apidocs/

Usage of the entrypoint: 
- Directly by the web interface via http://localhost:5000/getner
- By curl 
```shell
curl -F 'file=@document.pdf' localhost:5000/getner
```

