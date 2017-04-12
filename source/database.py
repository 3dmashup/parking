import psycopg2
from settings import get_settings


def database():
    """
    database establish as database connection and cursor
    :return: database cursor
    """
    settings = get_settings()
    connection = psycopg2.connect(dbname=settings['database']['dbame'],
                                  user=settings['database']['user'],
                                  password=settings['database']['password'],
                                  host=settings['database']['host'],
                                  port=settings['database']['port'])
    return connection.cursor()