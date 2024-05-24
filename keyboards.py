from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from googletrans import LANGUAGES



def start_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(text='Translate'),
        KeyboardButton(text='History')
    )
    return markup



def lang_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = []
    for lang in LANGUAGES.values():
        buttons.append(KeyboardButton(text=lang))

    markup.add(*buttons)
    return markup

