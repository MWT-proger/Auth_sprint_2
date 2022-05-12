FROM python:3.10-slim-buster

RUN mkdir -p /usr/src/fastapi
WORKDIR /usr/src/fastapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src  /src
WORKDIR /usr/src/fastapi/src

CMD ["gunicorn", "main:app","--workers","4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9000"]
