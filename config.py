import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DATABASE_DIR, exist_ok=True)
PATH_DATABASE = os.path.join(DATABASE_DIR, "db.trampoline")

SQLALCHEMY_DATABASE_URI = f"sqlite:///{PATH_DATABASE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
