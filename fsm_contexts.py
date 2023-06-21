from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    choose_language = State()
    choose_category = State()
    send_name = State()
    send_phone = State()
    send_address = State()
