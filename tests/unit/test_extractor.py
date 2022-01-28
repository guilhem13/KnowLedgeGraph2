import os

from model.extractorfrompdf import Extractor

lib_path = os.path.abspath("./")


def test_Exctractor():
    import sys

    print(sys.path)
    pdf = Extractor(lib_path + "/tests/unit/Test.pdf")
    assert pdf.title_file == lib_path + "/tests/unit/Test.pdf"
    assert pdf.number_of_pages == 12
