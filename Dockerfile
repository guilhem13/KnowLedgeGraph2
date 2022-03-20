# For more information, please refer to https://aka.ms/vscode-docker-python
FROM debian:11

EXPOSE 5000

#ENV key=venv

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN apt-get update -q -y
RUN apt-get install -yf \
    gcc python-dev libkrb5-dev python3-docopt python3-gssapi \
    python3 \
    python3-pip

RUN python3 -m pip install --upgrade pip
#RUN python3 pip install -U nltk
#RUN python -m nltk.downloader -q all
RUN python3 -m pip install -r requirements.txt
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader averaged_perceptron_tagger
RUN python3 -m nltk.downloader maxent_ne_chunker
RUN python3 -m nltk.downloader words


WORKDIR /ProjetPythonAPI
COPY . /ProjetPythonAPI

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /ProjetPythonAPI
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["python", "app.py"]

# execute the script:
CMD [ "python", "app.py" ]
