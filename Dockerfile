FROM python:3.8-slim as builder

ADD . /ProjetPythonAPI
WORKDIR /ProjetPythonAPI


COPY requirements.txt .
RUN apt update -q -y
RUN apt install -yf \
    apt-get install python-pip libkrb5-dev \
    build-essential libpoppler-cpp-dev pkg-config python3-dev \
    python3 \
    python3-pip
RUN python3 --version
RUN python3 -m pip install --upgrade pip
RUN pip3 install nltk
RUN [ "python", "-c", "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger');nltk.download('maxent_ne_chunker');nltk.download('words')" ]
RUN python3 -m pip install -r requirements.txt
#RUN python3 -m nltk.downloader punkt
#RUN python3 -m nltk.downloader averaged_perceptron_tagger
#RUN python3 -m nltk.downloader maxent_ne_chunker
#RUN python3 -m nltk.downloader words


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /ProjetPythonAPI
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["python", "app.py"]

# execute the script:
CMD [ "python", "app.py" ]
