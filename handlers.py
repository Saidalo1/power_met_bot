from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType

from config import start_message, LANGUAGES, bot, GROUP_CHAT_ID
from fsm_contexts import BotStates
from keyboards import languages_keyboard, select_category, cancel_keyboard, send_contact_keyboard, \
    send_location_keyboard
from utils import update_user_language, get_user_language, get_translate, send_location_to_chat, information_message


async def start(message: Message):
    if message.chat.type != ChatType.PRIVATE:
        return

    # Switch to the language selection state
    await BotStates.choose_language.set()

    # Respond to the message with the start_message text and use languages_keyboard as the reply_markup
    await message.answer(start_message, reply_markup=languages_keyboard())


async def select_language(message: Message, state: FSMContext):
    user_language = update_user_language(message.from_user.id, LANGUAGES[message.text])
    greeting_text = get_translate(user_language, 'GREETING_TEXT')
    select_category_kb = select_category(user_language)
    async with state.proxy() as data:
        data['user_language'] = user_language
    await BotStates.next()
    await message.answer(greeting_text, reply_markup=select_category_kb)


async def incorrect_select_language(message: Message):
    user_language = get_user_language(message.from_user.id)
    error_language = get_translate(user_language, 'ERROR_LANGUAGE')
    await message.answer(error_language, reply_markup=languages_keyboard())


async def consultation(message: Message, state: FSMContext):
    async with state.proxy() as data:
        current_language = data.get('user_language', 'en')
        send_name_text = get_translate(current_language, 'SEND_NAME_TEXT')
        await message.answer(send_name_text, reply_markup=cancel_keyboard(current_language))
    await BotStates.next()


async def got_name(message: Message, state: FSMContext):
    await BotStates.next()
    async with state.proxy() as data:
        data['user_name'] = message.text
        current_language = data.get('user_language', 'en')
        send_phone_text = get_translate(current_language, 'SEND_PHONE_TEXT')
        await message.answer(send_phone_text, reply_markup=send_contact_keyboard(current_language))


async def incorrect_got_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        current_language = data.get('user_language', 'en')
    error_language = get_translate(current_language, 'ERROR_NAME_TEXT')
    await message.answer(error_language, reply_markup=cancel_keyboard(current_language))


async def got_contact(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.contact.phone_number
        current_language = data.get('user_language', 'en')
    await BotStates.next()
    send_address_text = get_translate(current_language, 'SEND_ADDRESS_TEXT')
    await message.answer(send_address_text, reply_markup=send_location_keyboard(current_language))


async def got_address(message: Message, state: FSMContext):
    async with state.proxy() as data:
        user_name = data.get('user_name')
        contact = data.get('contact')
        location_latitude = message.location.latitude
        location_longitude = message.location.longitude
        current_language = data.get('user_language', 'en')
        await bot.send_message(GROUP_CHAT_ID,
                               information_message(user_name, contact))
        await send_location_to_chat(GROUP_CHAT_ID, location_latitude, location_longitude)
    select_category_kb = select_category(current_language)
    await BotStates.first()
    await message.answer(get_translate(current_language, 'GREETING_TEXT'), reply_markup=select_category_kb)
