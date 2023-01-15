FROM python:3.10.8

RUN pip install --upgrade pip


COPY requirements.txt .
RUN pip install -r requirements.txt



WORKDIR /app

COPY main.py /app
ENTRYPOINT python3 main.py