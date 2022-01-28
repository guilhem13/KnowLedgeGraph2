import json
import os

from celery import Celery
from flask import Response, jsonify, render_template, request
from werkzeug.utils import secure_filename

from __init__ import app
from model.extractorfrompdf import Extractor
from model.modelbdd import session_creator
from model.notificationmodel import Notification
from model.pdfmodel import Pdf

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    basedir, "basededonneepdf.db"
)  # URI where the database is located
ALLOWED_EXTENSIONS = {"txt", "pdf"}  # list of file extensions which can be downloaded

# configuration of app settings
app.config["UPLOAD_FOLDER"] = "."
app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"

# configuration of celery settings
app.config["CELERY_BROKER_URL"] = "amqp://username:siocbienG@localhost/"
app.config["CELERY_RESULT_BACKEND"] = "rpc://"
celery = Celery(
    app.name,
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"],
)

# create a session with the database
session = session_creator()


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
                    task = InjestPdf.apply_async([file.filename])
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


# Method which extracts metadata from the file and injests the data of the pdf inside the database with the session
@celery.task(bind=True, name="PdfApi.InjestPdf")
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
        session.add(pdf)
        session.commit()
        message = {"route": "file is being uploaded", "id": self.request.id}
    else:
        message = {"route": "file can't be parsed", "id": self.request.id}
    return json.dumps(message)


# route which allows users to get metadata from file
@app.route("/documents/<id>")
def taskstatus(id):
    task = InjestPdf.AsyncResult(id)
    # celery doesn't make the difference when the task is pending or the task doesn't exist. So we check inside the database
    if task.state == "PENDING":
        if (
            session.query(Pdf).filter(Pdf.id == id).scalar() is not None
        ):  # in Case of an other celery session
            status = session.query(Pdf).filter(Pdf.id == id).one()
            response = {
                "id": id,
                "state": task.state,
                "creation_date_of_file": str(status.creationdate),
                "author": str(status.author),
                "creator": str(status.creator),
                "producer": str(status.producer),
                "subject": str(status.subject),
                "title": str(status.title),
                "number_of_pages": str(status.number_of_pages),
                "keywords": str(status.keywords),
                "title_file": str(status.title_file),
                "timestamp_uploading": str(status.timestamp_uploading),
            }
            return response
        else:
            response = {
                "state": "Pending",
                "message": "Task is waiting for execution or unknown id. Any task id that’s not known is implied to be in the pending state.",
            }

    elif task.state == "FAILURE":
        response = {
            "state": "not completed",
        }
        response["result"] = task.info
    else:
        check = (
            session.query(Pdf).filter(Pdf.id == id).scalar() is not None
        )  # Query inside the database with pdf's id
        if check:
            status = session.query(Pdf).filter(Pdf.id == id).one()
            response = {
                "id": id,
                "state": task.state,
                "creation_date_of_file": str(status.creationdate),
                "author": str(status.author),
                "creator": str(status.creator),
                "producer": str(status.producer),
                "subject": str(status.subject),
                "title": str(status.title),
                "number_of_pages": str(status.number_of_pages),
                "keywords": str(status.keywords),
                "title_file": str(status.title_file),
                "timestamp_uploading": str(status.timestamp_uploading),
            }
    return jsonify(response)


# route which allows users to get text from file
@app.route("/text/<id>.txt")
def display_text(id):
    try:
        status = (
            session.query(Pdf).filter(Pdf.id == id).one()
        )  # Query inside the database with pdf's id
        response = {"text": str(status.data)}
        return jsonify(response)

    except Exception:
        return Response(
            Notification("4", "File id not in database").message(),
            status=400,
            mimetype="application/json",
        )


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


session.close()


if __name__ == "__main__":
    app.run(port=5000)
