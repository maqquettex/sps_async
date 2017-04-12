FROM python:3.6

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . /project

CMD ["python", "/project/manage.py"]