import os
import sys

import pytest

lib_path = os.path.abspath("./")
sys.path.append(lib_path)

from random import randrange

from model import pdfmodel
from model.modelbdd import session_creator
from webapp import app


@pytest.fixture
def create_app():
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_client():
    """A test client for the app."""
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def init_database():
    # Create the session and add to db
    session = session_creator()
    pdf = pdf = pdfmodel.Pdf(
        "pdfdetestpourpython4",
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
    yield session
