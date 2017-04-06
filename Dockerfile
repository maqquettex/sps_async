FROM python:3.6


RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 4000