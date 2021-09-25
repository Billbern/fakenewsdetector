import os
from dotenv import load_dotenv

dotenv_path = f'{os.getcwd()}/.env'
load_dotenv(dotenv_path)

class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")

