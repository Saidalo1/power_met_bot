from re import search

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType, CallbackQuery

from config import start_message, LANGUAGES, bot, GROUP_CHAT_ID, GENERATORS_PER_PAGE, default_language, \
    SALES_DEPARTMENT_PHONE_NUMBER, photo
from fsm_contexts import BotStates
from keyboards import languages_keyboard, select_category, cancel_keyboard, send_contact_keyboard, \
    send_location_keyboard, order_inline_keyboard
from models import session, Generator
from utils import update_user_language, get_user_language, get_translate, send_location_to_chat, information_message, \
    show_generators


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


async def calculation(message: Message, state: FSMContext):
    async with state.proxy() as data:
        current_language = data.get('user_language', default_language)
    await BotStates.calculations.set()

    # Загрузка всех генераторов в начале и сохранение их в переменной
    generators = session.query(Generator).order_by(Generator.power_kbT).limit(GENERATORS_PER_PAGE).all()
    total_generators = len(generators)

    start_index = 0
    page = 1

    async with state.proxy() as data:
        data['context'] = f"{start_index},{page},{total_generators}"

    await show_generators(message.chat.id, generators, start_index, page, total_generators, current_language)


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

        await show_generators(message.chat.id, generators, start_index, page,
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
        await show_generators(message.chat.id, generators, start_index, page,
                              total_generators, current_language)
        # Обновляем контекст состояния с новыми значениями
        await state.update_data(context=f"{start_index},{page},{total_generators}")


async def generator_selected(message: Message, state: FSMContext):
    data = await state.get_data()
    current_language = data.get('user_language', default_language)
    generator_name = search(r'\((.*?)\)', message.text).group(1).strip()
    generator = session.query(Generator).filter_by(name=generator_name).first()

    if generator:
        await message.answer_photo(photo,
                                   get_translate(current_language, "DETAIL_INFORMATION_ABOUT_GENERATOR") + f"\n\n" +
                                   get_translate(current_language, "TITLE_GENERATOR") + f"{generator.name}\n" +
                                   get_translate(current_language,
                                                 "POWER") + f"{generator.power_kbT} кВТ / {generator.power_kbA} кВА\n" +
                                   get_translate(current_language,
                                                 "FUEL_CONSUMPTION") + f"{generator.fuel_consumption} Л/ч\n" +
                                   get_translate(current_language, "HEIGHT") + f"{generator.height}\n" +
                                   get_translate(current_language, "LENGTH") + f"{generator.length}\n" +
                                   get_translate(current_language, "WIDTH") + f"{generator.width}",
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
        await message.answer("Назад в главное меню", reply_markup=languages_keyboard())
        await state.finish()
    elif current_state == BotStates.choose_category.state:
        await message.answer("Назад в меню выбора языка", reply_markup=languages_keyboard())
        await BotStates.previous()
    elif current_state == BotStates.send_name.state:
        await message.answer("Назад в меню выбора категории", reply_markup=select_category(current_language))
        await BotStates.previous()
    elif current_state == BotStates.send_phone.state:
        await message.answer("Пожалуйста, переотправьте ваше имя", reply_markup=cancel_keyboard(current_language))
        await BotStates.previous()
    elif current_state == BotStates.send_address.state:
        await message.answer("Пожалуйста, переотправьте ваш контакт",
                             reply_markup=send_contact_keyboard(current_language))
        await BotStates.previous()
    elif current_state == BotStates.calculations.state:
        await message.answer("Назад в меню выбора категории", reply_markup=select_category(current_language))
        await BotStates.choose_category.set()


async def main_menu(message: Message, state: FSMContext):
    await message.answer("Назад в главное меню", reply_markup=languages_keyboard())
    await BotStates.first()
