from dotenv import load_dotenv

from utils import os_environ_get

# Load env
load_dotenv()

# Telegram Bot Token
TOKEN = os_environ_get('TOKEN')

# Database settings
DATABASE_USER = os_environ_get('DATABASE_USER')
DATABASE_PASS = os_environ_get('DATABASE_PASS')
DATABASE_HOST = os_environ_get('DATABASE_HOST')
DATABASE_NAME = os_environ_get('DATABASE_NAME')
DATABASE_PORT = os_environ_get('DATABASE_PORT')

# Greeting Text
greeting_text = os_environ_get('GREETING_TEXT')

# Languages
LANGUAGES = {'English language 🇬🇧': 'en', 'Русский язык 🇷🇺': 'ru', 'O\'zbek tili 🇺🇿': 'uz'}
languages = tuple(LANGUAGES.keys())
