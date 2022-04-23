FROM python:3.10-slim-buster

RUN mkdir -p /usr/src/auth
WORKDIR /usr/src/auth

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

CMD flask db init && flask db migrate && flask db upgrade

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /src
WORKDIR /usr/src/auth/src

CMD ["gunicorn", "--chdir", "app", "main:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:5000"]
