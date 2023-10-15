FROM python:3.11-buster

WORKDIR /usr/src/moretech

EXPOSE 8080

ADD ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY . /usr/src/moretech/

CMD python -m uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
