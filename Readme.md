# Extract text from pdf 

It's a simple REST API which parse pdf file in order to extract text from it 

***

### Features included 

 - Feature 1 : Upload pdf and save its data into a database
        Endpoint : /documents
 - Feature 2 : Get the metadata from this uploading
        Endpoint : /documents/{id}
 - Feature 3 : Request the text of files uploaded by id
        Endpoint : /text/{id}.txt

***
## Installation 

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
********** TO DO *************
```

***
## Usage

#### Feature 1

##### On browser

Open http://localhost:5000/documents in a browser to upload your pdf 
![GitHub Logo](/images/documents.png)

***

###### Result 

Open http://localhost:5000/documents in a browser to upload your pdf 
![GitHub Logo](/images/document_return_id.png)

###### On Command 

```shell
curl -F 'file=@document.pdf' localhost:5000/documents
```
#### Feature 2

##### On browser

Open http://localhost:5000/documents in a browser to upload your pdf 
![GitHub Logo](/images/get-metadata.png)

##### On Command 

```shell
curl http://127.0.0.1:5000/documents/{id}
```
#### Feature 3 

##### On browser

Open http://localhost:5000/documents in a browser to upload your pdf 
![GitHub Logo](/images/Get-text.png)

##### On Command 

```shell
curl http://127.0.0.1:5000/text/{id}.txt
```



