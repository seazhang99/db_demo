from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from environs import Env

HC = {
    "endpoint" : "<Your HANA Cloud Instance Link>",
    "port" : 443,
    "user" : "<Your DB user>",
    "password" : "<Your DB password>"
}

EMBEDDING_PATH = './embedding'
MINILM_EMBEDDING = HuggingFaceEmbeddings(model_name=os.path.join(EMBEDDING_PATH, 'all-MiniLM-L6-v2'),
                                        model_kwargs={'device': 'cpu'})
JINA_EMBEDDING = 'jina'
DEFAULT_EMBEDDING_NAME = 'jina'

SCHEMA_FILE_PATH = './schema'
TMP_FILE_PATH = './tmp'

env = Env()
env.read_env()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    ENV = env("FLASK_ENV", "development")
    SECRET_KEY = '04ab47b6121745cf1400f91373c7b3cc'
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT", 0)
    CACHE_TYPE = env("CACHE_TYPE", "SimpleCache")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = env.int("APP_PORT", 5000)