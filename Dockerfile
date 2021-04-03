# fetches Python image based on Slim
FROM python:3.8-slim

# setup working directory
WORKDIR /app

# install requirements
COPY requirements.txt /
RUN pip install -U pip
RUN pip install -r /requirements.txt --no-cache-dir


# copy waiting script
COPY wait-for-it.sh /


# copy folder into working directory
COPY src/ /app




# Start app via run.py
#