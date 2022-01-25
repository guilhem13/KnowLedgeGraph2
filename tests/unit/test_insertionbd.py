

from model import pdfmodel

def test_bd(init_database):
    pdf = pdf = pdfmodel.Pdf(
        "12",
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
        "1643138913.3611"
    )
    response = init_database.query(pdf).filter(pdf.id == id).one()
    assert response.status_code == 200