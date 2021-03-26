#fetches Python image based on Alpine Linux
#FROM python:3.8-alpine
FROM python:3.8-slim

#setup working directory
WORKDIR /app

#install requirements
COPY requirements.txt /
RUN pip install -U pip
RUN pip install -r /requirements.txt --no-cache-dir

#copy folder into working directory
COPY src/ /app

#Start app via run.py
CMD /app/frontend/run.py