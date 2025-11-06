# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из файла .env

AUTHORIZED_USERNAME = os.getenv("AUTHORIZED_USERNAME")  # AUTHORIZED_USERNAME
AUTHORIZED_PASSWORD = os.getenv("AUTHORIZED_PASSWORD")  # AUTHORIZED_PASSWORD
