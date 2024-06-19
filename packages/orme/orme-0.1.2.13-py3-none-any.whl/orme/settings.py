import os


DATABASE_URL = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'orme.db')

QUERY_CREATE = 1
QUERY_LIST = 2
QUERY_UPDATE = 3
QUERY_DELETE = 4
