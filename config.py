import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode
from dotenv import load_dotenv


# OS Environment Variables
def os_environ_get(value):
    return os.environ.get(value)


# Load env
load_dotenv()

# Telegram Bot Token
TOKEN = os_environ_get('TOKEN')

# Telegram Bot
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=RedisStorage2('localhost', 6379, 0))

# Database settings
DATABASE_NAME = os_environ_get('DATABASE_NAME')

# Group Chat ID
GROUP_CHAT_ID = f"-100{os_environ_get('GROUP_CHAT_ID')}"

# Start Message
start_message = os_environ_get('START_MESSAGE')

# Languages
LANGUAGES = {'English language 🇬🇧': 'en', 'Русский язык 🇷🇺': 'ru', 'O\'zbek tili 🇺🇿': 'uz'}
languages = tuple(LANGUAGES.keys())
lang_values = tuple(LANGUAGES.values())

# Default Language
default_language = LANGUAGES.get('English language 🇬🇧', 'ru')

# Locale Directory
LOCALE_DIRECTORY = os_environ_get('LOCALE_DIRECTORY')

# Generators per page
GENERATORS_PER_PAGE = int(os_environ_get('GENERATORS_PER_PAGE'))

# Sales Department Number
SALES_DEPARTMENT_PHONE_NUMBER = os_environ_get('SALES_DP_NUM')

# Media URL
MEDIA_FOLDER_NAME = os.path.dirname(os.path.abspath(__file__)) + os_environ_get('MEDIA_FOLDER_NAME')

current_directory = os.path.dirname(os.path.abspath(__file__))

# Формируйте путь к файлу с учетом текущей директории и папки media
photo_path = os.path.join(current_directory, 'media')
