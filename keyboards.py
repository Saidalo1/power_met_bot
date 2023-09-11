from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import query

from config import languages
from utils import get_translate


def order_inline_keyboard(current_language) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(get_translate(current_language, "ORDER"), callback_data='order'))


def cancel_keyboard(language) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[KeyboardButton(get_translate(language, 'BACK'))]], True)


def send_contact_keyboard(language) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[KeyboardButton(get_translate(language, 'SEND_CONTACT'), request_contact=True),
                                 KeyboardButton(get_translate(language, 'BACK'))]], True)


def send_location_keyboard(language) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[KeyboardButton(get_translate(language, 'SEND_LOCATION'), request_location=True),
                                 KeyboardButton(get_translate(language, 'BACK'))]], True)


# Languages Keyboard
def languages_keyboard() -> ReplyKeyboardMarkup:
    languages_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    buttons = [(KeyboardButton(text=lang)) for lang in languages]
    languages_kb.add(*buttons)
    return languages_kb


def select_category(language) -> ReplyKeyboardMarkup:
    categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    buttons = [(get_translate(language, "CONSULT")),
               (get_translate(language, "CATALOG")), ]
    categories_kb.add(*buttons)
    categories_kb.add(KeyboardButton(get_translate(language, 'BACK')))
    return categories_kb


def categories_of_generators_kb(language, generators: query) -> ReplyKeyboardMarkup:
    categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    buttons = [generator.name for generator in generators]
    categories_kb.add(*buttons)
    categories_kb.add(KeyboardButton(get_translate(language, 'BACK')))
    return categories_kb
