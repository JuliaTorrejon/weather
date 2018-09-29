FROM python:alpine

WORKDIR /opt/src/weather

ADD requirements.txt requirements.txt
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ADD weather.py weather.py

ENTRYPOINT ["python3", "weather.py"]