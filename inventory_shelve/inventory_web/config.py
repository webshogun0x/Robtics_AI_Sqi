import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ESP32_UNLOCK_URL = os.environ.get('ESP32_UNLOCK_URL') or 'http://shelf-locker.local/unlock'
