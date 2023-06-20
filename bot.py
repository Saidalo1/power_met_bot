from aiogram import Dispatcher, Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

from config import TOKEN, languages
from handlers import start, select_service_type

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# Add LifetimeControllerMiddleware to ensure the storage is cleared correctly on restart
dp.middleware.setup(LoggingMiddleware())

# Register the handlers
dp.register_message_handler(start, commands='start')
dp.register_message_handler(select_service_type, lambda message: message.text in languages)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
