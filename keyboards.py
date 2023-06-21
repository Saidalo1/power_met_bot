from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import languages
from utils import get_translate


def cancel_keyboard(language) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[KeyboardButton(get_translate(language, 'CANCEL'))]], True, True)


def send_contact_keyboard(language) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[KeyboardButton(get_translate(language, 'SEND_CONTACT'), request_contact=True)]], True,
                               True)


def send_location_keyboard(language) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[KeyboardButton(get_translate(language, 'SEND_LOCATION'), request_location=True)]],
                               True,
                               True)


# Languages Keyboard
def languages_keyboard() -> ReplyKeyboardMarkup:
    languages_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    buttons = [(KeyboardButton(text=lang)) for lang in languages]
    languages_kb.add(*buttons)
    return languages_kb


def select_category(language) -> ReplyKeyboardMarkup:
    categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    buttons = [(get_translate(language, "CONSULT")),
               (get_translate(language, "CALCULATE"))]
    categories_kb.add(*buttons)
    return categories_kb
