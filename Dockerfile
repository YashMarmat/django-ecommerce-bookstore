FROM python:3.11.3-bullseye

RUN apt-get update && apt-get upgrade -y

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .