import os

from settings import INIT_DB_CMD


def init_db():
    os.system(INIT_DB_CMD)
