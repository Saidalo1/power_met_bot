import gettext

from config import lang_values, LOCALE_DIRECTORY

translators = {}
for lang in lang_values:
    translator = gettext.translation('messages', localedir=LOCALE_DIRECTORY, languages=[lang])
    translator.install()
    translators[lang] = translator
