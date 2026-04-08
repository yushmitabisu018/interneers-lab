import os
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()
def init_db():
    uri = os.environ.get("MONGODB_URI")

    connect(host=uri)