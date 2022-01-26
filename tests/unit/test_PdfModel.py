import os
import sys

from model import pdfmodel


def test_Pdf():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    pdf = pdfmodel.Pdf(
        "pdftest",
        "data",
        "titre du pdf",
        "08/10/1998",
        "Guilhem Maillebuau",
        "pierre",
        "Léon borrelly",
        "climate change",
        "nature",
        23,
        "monfichier.pdf",
        "1643134545.3611",
    )
    assert pdf.name == "pdftest"
    assert pdf.data == "data"
    assert pdf.title == "titre du pdf"
    assert pdf.creationdate == "08/10/1998"
    assert pdf.author == "Guilhem Maillebuau"
    assert pdf.creator == "pierre"
    assert pdf.producer == "Léon borrelly"
    assert pdf.subject == "climate change"
    assert pdf.keywords == "nature"
    assert pdf.number_of_pages == 23
    assert pdf.title_file == "monfichier.pdf"
    assert pdf.timestamp_uploading == "1643134545.3611"
