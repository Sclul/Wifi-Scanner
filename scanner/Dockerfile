FROM python:latest


RUN apt-get update && apt-get install -y python3 python3-pip 
RUN pip3 install numpy && pip3 install gpsdclient
RUN apt-get install -y wireless-tools &&  apt-get install net-tools


WORKDIR /app

COPY scanner.py /app
ENTRYPOINT python3 scanner.py


