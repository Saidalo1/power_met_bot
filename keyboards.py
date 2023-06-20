from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import languages


# Languages Keyboard
def languages_keyboard() -> ReplyKeyboardMarkup:
    languages_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    buttons = [(KeyboardButton(text=lang)) for lang in languages]
    languages_kb.add(*buttons)
    return languages_kb
