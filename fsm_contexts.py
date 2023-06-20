from aiogram.dispatcher.filters.state import State, StatesGroup


class LanguageState(StatesGroup):
    choose_language = State()
