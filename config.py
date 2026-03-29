import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_DATABASE = os.path.join(BASE_DIR, "database", 'db.trampoline')

os.makedirs(PATH_DATABASE, exist_ok=True)

SQLALCHEMY_DATABASE_URI = f"sqlite:///{PATH_DATABASE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
