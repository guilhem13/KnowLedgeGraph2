import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
import json
import os
import flask
import appmanager
from flask import Response, render_template, request
from werkzeug.utils import secure_filename
from nlpmodel import service_one_extraction
from models.notificationmodel import Notification
from controller import Data,Textprocessed
from owl import ontology


app = flask.Flask(__name__)
app.config["UPLOAD_FOLDER"] = "."


# Route where the client wants to get ner from an uploading pdf 
@app.route("/getner", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:  # no file part
            return Response(
                Notification("1", "No file part").message(),
                status=400,
                mimetype="application/json",
            )
        else:
            file = request.files["file"]  # No selected file
            if file.filename == "":
                return Response(
                    Notification("400", "No selected file").message(),
                    status=400,
                    mimetype="application/json",
                )
            else:
                if file and appmanager.allowed_file(file.filename):  # Check if the file has the correct extension
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    ners = service_one_extraction.ServiceOne(Textprocessed(None).get_data_from_file(filename)).get_references()
                    os.remove(filename)
                    return json.dumps([ob.__dict__ for ob in ners])                      
                else:
                    return Response(
                        Notification("3", "File type not permitted").message(),
                        status=400,
                        mimetype="application/json",
                    )
    return render_template("index.html")

@app.route("/arxiv/generatepipeline/<nb_paper>")
def create_pipeline(nb_paper):
    nb_paper_to_request = int(nb_paper)
    block_arxiv_size = 5
    arxiv_data = Data(nb_paper_to_request).get_set_data()
    papiers= []
    for i in range(0,len(arxiv_data),block_arxiv_size):
        print(i) 
        papiers+= appmanager.arxiv_route_main_function(arxiv_data[i:i+block_arxiv_size])
    owl = ontology.Ontology()
    for papier in papiers: 
        owl.add_papier(papier)
    owl.save('result.owl') #TODO retourner en mode json 
    return Response(
                    Notification("200", str(owl.get_ontology())).message(),
                    status=400,
                    mimetype="application/json",
                )
    

############################### Error handler ########################################
# route for error 500
@app.errorhandler(500)
def internal_server_errors(error):
    return Response(
        Notification(
            "404",
            "error :/ Internal Server Error",
        ).message(),
        status=404,
        mimetype="application/json",
    )


# route for error 404
@app.errorhandler(404)
def internal_server_error(error):
    return Response(
        Notification(
            "404",
            "Sorry wrong endpoint.This endpoint doens't exist. Check your endpoint or your id arguments",
        ).message(),
        status=404,
        mimetype="application/json",
    )
##########################################################################################


if __name__ == "__main__":
    app.run(port=5000)
