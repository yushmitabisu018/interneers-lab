from mongoengine import connect, disconnect
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    try:
        disconnect()
    except Exception:
        pass

    uri = os.getenv("MONGO_URI")
    connect(host=uri)