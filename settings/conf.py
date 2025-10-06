# Project modules
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = 'django-insecure-f%lu)5s5)sh8bc2ng*3on+ajts)*b7$1^i$l7$_zfe9_k@w!0)'

# -------------- ENV SETTINGS ------------------------
ENV_POSSIBLE_OPTIONS = [
    "local",
    "prod",
]

ENV_ID = os.getenv("DJANGORLAR_ENV_ID", "local")
