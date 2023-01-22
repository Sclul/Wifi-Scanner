FROM python:latest


RUN apt-get update && apt-get install -y python3 python3-pip 
RUN apt-get install -y wireless-tools &&  apt-get install net-tools

COPY requirements.txt .
RUN pip install -r requirements.txt


WORKDIR /app

COPY scanner.py /app
ENTRYPOINT python3 scanner.py


