FROM python:3.6

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD ./sps /sps

CMD ["python", "/sps/manage.py"]