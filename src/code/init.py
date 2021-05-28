# run.py
import psycopg2
import time
import logging

from app.biblio import Biblio


def try_init(retries=10):
    """
    ###DEPRECATED###
    Tries to establish a connection to the database and initialises the database if connection was successful.
    Can only be used from outside of a docker container with a database listening on localhost:5432.

    :param retries:
    :return int:
    """
    calc_retries = retries
    connection = False
    # Do Loop while there are still retries available and the database is not connected
    while retries > 0 and connection is False:
        try:
            con = psycopg2.connect(database="postgres", user="postgres", port=5432,
                                   password="1234", host="localhost")
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
