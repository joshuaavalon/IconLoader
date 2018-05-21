FROM python:alpine

RUN mkdir /data

COPY ./* /data/

WORKDIR /data

RUN pip install -r requirements.txt

CMD ["python", "app.py"]