from aiogram.types import Message

from config import greeting_text
from fsm_contexts import LanguageState
from keyboards import languages_keyboard
from messages_text import start_message


async def start(message: Message):
    # Switch to the language selection state
    await LanguageState.choose_language.set()

    # Respond to the message with the start_message text and use languages_keyboard as the reply_markup
    await message.answer(start_message, reply_markup=languages_keyboard())


async def select_service_type(message: Message):
    await message.answer(greeting_text)
