from re import match

from aiogram.utils.exceptions import BotBlocked, ChatNotFound, RetryAfter, ChatAdminRequired, TelegramAPIError

from config import default_language, bot
from models import session, UserLanguage
from translations import translators


def get_user_language(user_id):
    user = session.query(UserLanguage).filter_by(chat_id=user_id).first()
    if user is None:
        user = UserLanguage(user_id, default_language)
        session.add(user)
        session.commit()
    return user.language


def update_user_language(user_id, language):
    user = session.query(UserLanguage).filter_by(chat_id=user_id).first()
    if user is None:
        user = UserLanguage(user_id, default_language)
        session.add(user)
        session.commit()
    else:
        if user.language != language:
            user.language = language
            session.commit()
    return user.language


def get_translate(language, phrase):
    return translators[language if language else default_language].gettext(phrase)


def is_valid_name(name):
    if len(name) < 3 or len(name) > 30 or not match(r'^[a-zA-Zа-яА-ЯёЁ]+$', name):
        return False
    return True


async def send_location_to_chat(chat_id, latitude, longitude):
    try:
        await bot.send_location(chat_id, latitude, longitude)
    except BotBlocked:
        print(f"Bot is blocked by the chat_id {chat_id}")
    except ChatNotFound:
        print(f"Chat not found for chat_id {chat_id}")
    except RetryAfter as e:
        print(f"RetryAfter {e.timeout} for chat_id {chat_id}")
    except ChatAdminRequired:
        print(f"Chat admin required for chat_id {chat_id}")
    except TelegramAPIError:
        print(f"Failed to send location to chat_id {chat_id}")


def information_message(user_full_name, user_phone_number):
    return f' ✨ Новый пользователь ✨\n' \
           f'👤 Имя: {user_full_name} \n' \
           f'📞 Контакт: {user_phone_number} \n' \
