import os

from model.extractorfrompdf import Extractor

lib_path = os.path.abspath("./")

""" test to extract meta data from file """


def test_exctractor():

    pdf = Extractor(lib_path + "/tests/unit/Test.pdf")
    assert pdf.title_file == lib_path + "/tests/unit/Test.pdf"
    assert pdf.number_of_pages == 12
