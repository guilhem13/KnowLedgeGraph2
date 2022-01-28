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
Install Rabbitmq 

```shell
docker run -d --name some-rabbit -p 5672:5672 -p 5673:5673 -p 15672:15672 rabbitmq:3-management
```
Once installed, check if the rabbitmq container is running with 

```shell 
sudo docker ps 
```

if your container is not running 

```shell
sudo docker start  {your container id}
```

***

If the container works, you have to add an user.

* Go to http://localhost:15672/. Log in with => "username" : guest , "password" : guest 
* Go to the "Admin" bar at the top of the front page. Once there, add a user with "username" : username , "password" : siocbienG 
* Once you have created your user. The user will appear inside your user table . Click on the user you have created ( inside the table) and click on all "set permission" and "set topic permission" bar.  

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
## Usage

#### Feature 1

##### On browser

Open http://localhost:5000/documents in a browser to upload your pdf 
![GitHub Logo](/images/documents.png)

##### On Command 

```shell
curl -F 'file=@document.pdf' localhost:5000/documents
```
***

###### Result 

![GitHub Logo](/images/document_return_id.png)

{
   
    "task_id": [id],<br />
}
  * "task_id" : id of pdf which is being uploaded 

***
#### Feature 2

##### On browser

Open http://localhost:5000/documents in a browser to upload your pdf 
![GitHub Logo](/images/get-metadata.png)

##### On Command 

```shell
curl http://127.0.0.1:5000/documents/{id}
```
***
###### Result 
{
    # Auhtor of the pdf file in metadata pdf file : String
    "author": "[author]",
    # Date when the file was created by the author ; pdf file metadata: String
    "creation_date_of_file": "[date]",
    # creator of the pdf, what the author use : String
    "creator":"[creator]"
    # id of the file 
    "id": "[id]" : String
    #Keywords of the file inside metadata file
    "keywords" : "[keywords]" : String
    # Number of pages 
    "number_of_pages":[integer] : Integer
    # May be "SUCCESS", "PENDING" or "ERROR" (str)
    "status": "[status]",    

}

***
#### Feature 3 

##### On browser

Open http://localhost:5000/documents in a browser to upload your pdf 
![GitHub Logo](/images/Get-text.png)

##### On Command 

```shell
curl http://127.0.0.1:5000/text/{id}.txt
```



