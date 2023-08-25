from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    choose_language = State()
    choose_category = State()
    send_name = State()
    send_phone = State()
    send_address = State()
    calculations = State()


class SpreadingMessages(StatesGroup):
    send_message_uz = State()
    send_message_ru = State()
    send_message_en = State()
