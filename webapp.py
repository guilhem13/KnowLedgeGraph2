import json
import os
import flask
from flask import Response, jsonify, render_template, request
from werkzeug.utils import secure_filename
from controller.extractorfrompdf import Extractor
from model.notificationmodel import Notification
from model.pdfmodel import Pdf

import flask

app = flask.Flask(__name__)



basedir = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = {"pdf"}  # list of file extensions which can be downloaded

# configuration of app settings
app.config["UPLOAD_FOLDER"] = "."
#app.secret_key = "super secret key"
#app.config["SESSION_TYPE"] = "filesystem"


# Method witch checks if the file is allowed to be download
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Route where the client can download his file
@app.route("/documents", methods=["GET", "POST"])
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
                if file and allowed_file(
                    file.filename
                ):  # Check if the file has the correct extension
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    os.remove(filename)
                    task = InjestPdf(file.filename)
                    return Response(
                        json.dumps({"task_id": task.id}),
                        status=202,
                        mimetype="application/json",
                    )
                else:
                    return Response(
                        Notification("3", "File type not permitted").message(),
                        status=400,
                        mimetype="application/json",
                    )

    return render_template("index.html")


def InjestPdf(self, file):
    PdfProcessed = Extractor(file)
    if getattr(PdfProcessed, "extracted") is True:
        pdf = Pdf(
            getattr(PdfProcessed, "pdf_path"),
            getattr(PdfProcessed, "text_from_pdf"),
            getattr(PdfProcessed, "title"),
            getattr(PdfProcessed, "creationdate"),
            getattr(PdfProcessed, "author"),
            getattr(PdfProcessed, "creator"),
            getattr(PdfProcessed, "producer"),
            getattr(PdfProcessed, "subject"),
            getattr(PdfProcessed, "keywords"),
            getattr(PdfProcessed, "number_of_pages"),
            getattr(PdfProcessed, "title_file"),
            getattr(PdfProcessed, "timestamp_uploading"),
        )
        setattr(pdf, "id", self.request.id)
        message = {"route": "file is being uploaded", "id": self.request.id}
    else:
        message = {"route": "file can't be parsed", "id": self.request.id}
    return json.dumps(message)


"""
    except Exception:
        return Response(
            Notification("4", "File id not in database").message(),
            status=400,
            mimetype="application/json",
        )"""


# route for error 500
@app.errorhandler(500)
def internal_server_errors(error):
    return jsonify({"error": ":/ Internal Server Error"}), 500


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

if __name__ == "__main__":
    app.run(port=5000)
