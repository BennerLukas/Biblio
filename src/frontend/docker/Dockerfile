FROM python:3.8-alpine

ENV PYTHONBUFFERED 1

RUN mkdir /dockerised example

WORKDIR /dockerised example

ADD requirements.txt /dockerised-example/

# Install dependencies
RUN \
    # Install curl
    apk add --no-cache curl && \
    # Install postgres utilities which are required by `psycopg2` lib being used by app
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    # Install Python packages required by the app
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

ADD ./ /dockerised-example/
COPY docker/entrypoint.sh /sbin/entrypoint.sh    

EXPOSE 5000

ENTRYPOINT ["/sbin/entrypoint.sh"]
