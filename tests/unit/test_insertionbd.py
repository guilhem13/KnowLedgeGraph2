from random import randrange

from model import pdfmodel
from model.modelbdd import session_creator
from model.pdfmodel import Pdf

""" test to check if the file is correcty stored in the db """


def test_bd(init_database):
    session = session_creator()
    test = str(randrange(10000))
    pdf = pdf = pdfmodel.Pdf(
        test,
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
        "timestamp",
    )
    setattr(pdf, "id", str(randrange(10000)))
    session.add(pdf)
    session.commit()
    session.close()
    response = init_database.query(Pdf).filter(Pdf.name == test).one()
    assert response.timestamp_uploading == "timestamp"
