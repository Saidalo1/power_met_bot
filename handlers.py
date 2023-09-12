from re import search

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType, CallbackQuery
from sqlalchemy import asc
from sqlalchemy.exc import NoResultFound

from config import start_message, LANGUAGES, bot, GROUP_CHAT_ID, GENERATORS_PER_PAGE, default_language, \
    SALES_DEPARTMENT_PHONE_NUMBER, photo_path
from fsm_contexts import BotStates, SpreadingMessages
from keyboards import languages_keyboard, select_category, cancel_keyboard, send_contact_keyboard, \
    send_location_keyboard, order_inline_keyboard, categories_of_generators_kb
from models import session, Generator, Category  # , UserLanguage
from utils import update_user_language, get_user_language, get_translate, send_location_to_chat, information_message, \
    show_generators_fc


async def start(message: Message):
    if message.chat.type != ChatType.PRIVATE:
        return

    # Switch to the language selection state
    await BotStates.choose_language.set()

    # Respond to the message with the start_message text and use languages_keyboard as the reply_markup
    await message.answer(start_message, reply_markup=languages_keyboard())


async def start_in_state(message: Message, state: FSMContext):
    if message.chat.type != ChatType.PRIVATE:
        return

    await state.finish()
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
        current_language = data.get('user_language', default_language)
        send_name_text = get_translate(current_language, 'SEND_NAME_TEXT')
        await message.answer(send_name_text, reply_markup=cancel_keyboard(current_language))
    await BotStates.next()


async def got_name(message: Message, state: FSMContext):
    await BotStates.next()
    async with state.proxy() as data:
        data['user_name'] = message.text
        current_language = data.get('user_language', default_language)
        send_phone_text = get_translate(current_language, 'SEND_PHONE_TEXT')
        await message.answer(send_phone_text, reply_markup=send_contact_keyboard(current_language))


async def incorrect_got_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        current_language = data.get('user_language', default_language)
    error_language = get_translate(current_language, 'ERROR_NAME_TEXT')
    await message.answer(error_language, reply_markup=cancel_keyboard(current_language))


async def got_contact(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.contact.phone_number
        current_language = data.get('user_language', default_language)
    await BotStates.next()
    send_address_text = get_translate(current_language, 'SEND_ADDRESS_TEXT')
    await message.answer(send_address_text, reply_markup=send_location_keyboard(current_language))


async def got_address(message: Message, state: FSMContext):
    async with state.proxy() as data:
        user_name = data.get('user_name')
        contact = data.get('contact')
        location_latitude = message.location.latitude
        location_longitude = message.location.longitude
        current_language = data.get('user_language', default_language)
        await bot.send_message(GROUP_CHAT_ID,
                               information_message(user_name, contact))
        await send_location_to_chat(GROUP_CHAT_ID, location_latitude, location_longitude)
    select_category_kb = select_category(current_language)
    await BotStates.first()
    await message.answer(get_translate(current_language, 'GREETING_TEXT'), reply_markup=select_category_kb)


async def show_generators(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            current_language = data.get('user_language', default_language)
        message_text = get_translate(current_language, message.text)
        selected_category = session.query(Category).filter(Category.name == message_text).one()
        selected_category_id = selected_category.id
        await BotStates.selected_category_of_generators.set()

        generators = session.query(Generator).filter_by(category_id=selected_category_id).order_by(
            Generator.fuel_consumption).limit(GENERATORS_PER_PAGE).all()
        total_generators = len(generators)

        start_index = 0
        page = 1

        async with state.proxy() as data:
            data['context'] = f"{start_index},{page},{total_generators}"

        await show_generators_fc(message.chat.id, generators, start_index, page, total_generators, current_language)
    except NoResultFound:
        pass


async def show_categories_catalog(message: Message, state: FSMContext):
    async with state.proxy() as data:
        current_language = data.get('user_language', default_language)
    await BotStates.show_categories_of_generators.set()

    categories = session.query(Category).all()

    kb = categories_of_generators_kb(current_language, categories)

    await message.answer(get_translate(current_language, 'CHOOSE_CATEGORY_OF_GENERATORS'), reply_markup=kb)


async def next_page(message: Message, state: FSMContext):
    async with state.proxy() as data:
        current_language = data.get('user_language', default_language)
        context = await state.get_data()
        context = context.get('context')

    if context:
        start_index, page, total_generators = map(int, context.split(','))
        generators = session.query(Generator).all()
        start_index += GENERATORS_PER_PAGE  # Вычисляем новое значение start_index
        page += 1  # Увеличиваем значение page на 1

        if start_index >= total_generators:
            return  # Достигнуты крайние значения, прекращаем выполнение

        await show_generators_fc(message.chat.id, generators, start_index, page,
                                 total_generators, current_language)

        # Обновляем контекст состояния с новыми значениями
        await state.update_data(context=f"{start_index},{page},{total_generators}")


async def previous_page(message: Message, state: FSMContext):
    async with state.proxy() as data:
        current_language = data.get('user_language', default_language)
        context = await state.get_data()
    context = context.get('context')
    if context:
        start_index, page, total_generators = map(int, context.split(','))
        generators = session.query(Generator).all()
        start_index -= GENERATORS_PER_PAGE  # Вычисляем новое значение start_index
        page -= 1  # Уменьшаем значение page на 1
        await show_generators_fc(message.chat.id, generators, start_index, page,
                                 total_generators, current_language)
        # Обновляем контекст состояния с новыми значениями
        await state.update_data(context=f"{start_index},{page},{total_generators}")


async def generator_selected(message: Message, state: FSMContext):
    data = await state.get_data()
    current_language = data.get('user_language', default_language)
    generator_name = search(r'\((.*?)\)', message.text).group(1).strip()
    generator = session.query(Generator).filter_by(name=generator_name).first()
    photo_file_path = f'{photo_path}/' + f'{generator.category.image}'
    with open(photo_file_path, 'rb') as photo_file:
        photo = photo_file.read()

    if generator:
        await message.answer_photo(photo,
                                   get_translate(current_language, "TITLE_GENERATOR") + f"{generator.name}\n" +
                                   get_translate(current_language,
                                                 "POWER") + f"(кВТ/кВА): {generator.power} \n" +
                                   get_translate(current_language,
                                                 generator.category.generator_field_name) + f": {generator.fuel_consumption}\n" +
                                   get_translate(current_language,
                                                 "FUEL_TYPE") + f"{get_translate(current_language, str(generator.engine_type))}\n" +
                                   get_translate(current_language,
                                                 "HEIGHT_LENGTH_WIDTH") + f"{generator.size}",
                                   reply_markup=order_inline_keyboard(current_language))
    else:
        await message.reply(get_translate(current_language, "GENERATOR NOT FOUND"))


async def order_message(query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_language = data.get('user_language', default_language)
    info_text = get_translate(user_language, 'CALL_FOR_ORDER') + f'{SALES_DEPARTMENT_PHONE_NUMBER}'

    await bot.answer_callback_query(query.id, info_text, True)


async def back_to_main_menu(message: Message, state: FSMContext):
    current_state = await state.get_state()
    async with state.proxy() as data:
        current_language = data.get('user_language', default_language)

    if current_state == BotStates.choose_language.state:
        await message.answer(get_translate(current_language, "BACK_MAIN_MENU"), reply_markup=languages_keyboard())
        await state.finish()
    elif current_state == BotStates.choose_category.state:
        await message.answer(get_translate(current_language, "BACK_TO_MENU_SELECT_LANGUAGE"),
                             reply_markup=languages_keyboard())
        await BotStates.previous()
    elif current_state == BotStates.show_categories_of_generators.state:
        await message.answer(get_translate(current_language, 'GREETING_TEXT'),
                             reply_markup=select_category(current_language))
        await BotStates.choose_category.set()
    elif current_state == BotStates.send_name.state:
        await message.answer(get_translate(current_language, "BACK_TO_MENU_SELECT_CATEGORY"),
                             reply_markup=select_category(current_language))
        await BotStates.previous()
    elif current_state == BotStates.send_phone.state:
        await message.answer(get_translate(current_language, "RESEND_YOUR_NAME"),
                             reply_markup=cancel_keyboard(current_language))
        await BotStates.previous()
    elif current_state == BotStates.send_address.state:
        await message.answer(get_translate(current_language, "RESEND_YOUR_CONTACT"),
                             reply_markup=send_contact_keyboard(current_language))
        await BotStates.previous()
    elif current_state == BotStates.selected_category_of_generators.state:
        await message.answer(get_translate(current_language, 'CHOOSE_CATEGORY_OF_GENERATORS'),
                             reply_markup=categories_of_generators_kb(current_language, session.query(Category).all()))
        await BotStates.show_categories_of_generators.set()


async def main_menu(message: Message, state: FSMContext):
    async with state.proxy() as data:
        current_language = data.get('user_language', default_language)
    await message.answer(get_translate(current_language, "BACK_MAIN_MENU"), reply_markup=languages_keyboard())
    await BotStates.first()


async def send_message_to_all_users_get(message: Message, state: FSMContext):
    async with state.proxy() as data:
        current_language = data.get('user_language', default_language)
    await SpreadingMessages.send_message_uz.set()
    send_address_text = get_translate(current_language, 'SEND_SPREADING_MESSAGE_UZ')
    await message.answer(send_address_text, reply_markup=cancel_keyboard(current_language))

# async def send_message_to_all_users_uz(message: Message, state: FSMContext):
#     async with state.proxy() as data:
#         current_language = data.get('user_language', default_language)
#         data['message_in_uz_lang'] = message.text
#     await SpreadingMessages.send_message_ru()
#     send_address_text = get_translate(current_language, 'SEND_SPREADING_MESSAGE_RU')
#     await message.answer(send_address_text, reply_markup=cancel_keyboard(current_language))
#
#
# async def send_message_to_all_users_ru(message: Message, state: FSMContext):
#     async with state.proxy() as data:
#         current_language = data.get('user_language', default_language)
#         data['message_in_ru_lang'] = message.text
#     await SpreadingMessages.send_message_en.set()
#     send_address_text = get_translate(current_language, 'SEND_SPREADING_MESSAGE_EN')
#     await message.answer(send_address_text, reply_markup=cancel_keyboard(current_language))
#
#
# async def get_message_to_send_to_all_users(message: Message, state: FSMContext):
#     async with state.proxy() as data:
#         current_language = data.get('user_language', default_language)
#         message_in_en_lang = message.text
#         message_in_uz_lang = data.get('message_in_uz_lang')
#         message_in_ru_lang = data.get('message_in_ru_lang')
#
#     all_user_languages = await session.query(UserLanguage).all()
#
#     chat_ids_by_language = {}
#     for user_language in all_user_languages:
#         language = user_language.language
#         chat_id = user_language.chat_id
#         if language not in chat_ids_by_language:
#             chat_ids_by_language[language] = []
#         chat_ids_by_language[language].append(chat_id)
#
#     messages_by_language = {
#         'uz': message_in_uz_lang,
#         'ru': message_in_ru_lang,
#         'en': message_in_en_lang
#     }
#
#     for language, chat_ids in chat_ids_by_language.items():
#         message_text = messages_by_language[language]
#         if not message_text:
#             continue
#
#         batch_size = 50
#
#         async def send_message_batch(user_batch):
#             for user_chat_id in user_batch:
#                 try:
#                     await bot.send_message(user_chat_id, message_text)
#                 except Exception as e:
#                     print(f"Failed to send message to user with chat_id={user_chat_id}. Error: {e}")
#
#         for i in range(0, len(chat_ids), batch_size):
#             users_batch = chat_ids[i:i + batch_size]
#             await send_message_batch(users_batch)
#
#     successfully_spread_text = get_translate(current_language, 'SUCCESSFULLY_SENT_SPREAD_TEXT')
#     await message.answer(successfully_spread_text)
