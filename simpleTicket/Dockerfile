FROM python:3.10.0-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./Pipfile /usr/src/app/
COPY ./Pipfile.lock /usr/src/app/
RUN apt-get clean
RUN apt-get -y update
RUN apt-get -y install python3-dev build-essential
RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system
COPY . /usr/src/app/


