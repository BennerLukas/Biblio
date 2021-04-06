# run.py
import psycopg2
import time
import logging

from app.biblio import Biblio


def try_init(retries=10):
    calc_retries = retries
    connection = False
    while retries > 0 and connection is False:
        try:
            con = psycopg2.connect(database="postgres", user="postgres", port=5432,
                                   password="1234", host="database")
        except psycopg2.OperationalError:
            retries -= 1
            logging.error(f"Could not connect to database during initialization try {-1 * retries + calc_retries}")
            time.sleep(5)
        else:
            retries -= 1
            connection = True
            return retries


if __name__ == '__main__':
    logging.error("Init called")
    count = try_init()
    logging.info(f"Remaining retries: {count}")
    logging.error("Connection possible -- trying to initialize database")
    Biblio().init_db()
