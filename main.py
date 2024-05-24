import os
from dotenv import load_dotenv
from telebot import TeleBot, types
from googletrans import Translator, LANGCODES
import keyboards as kb
import database as db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

translator = Translator()

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    db.insert_user(chat_id)
    bot.send_message(chat_id,
                     "привет я бот для перевода",
                     reply_markup=kb.start_menu()
                     )


@bot.message_handler(commands=['help'])
def command_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     "Чем я могу вам помочь",
                     reply_markup=kb.start_menu()
                     )
@bot.message_handler(func=lambda msq: msq.text == 'Translate')
def start_translation(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык',
                     reply_markup=kb.lang_menu()
                     )
    bot.register_next_step_handler(message, get_lang_from)

def get_lang_from(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Выберите язык:",
                     reply_markup=kb.lang_menu()
                     )
    bot.register_next_step_handler(message, get_lang_to, message.text)

def get_lang_to(message, lang_from):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Напишите слово или текст',
                     reply_markup=types.ReplyKeyboardRemove()
                     )
    bot.register_next_step_handler(message, translate, lang_from, message.text)


def translate(message, lang_from, lang_to):
    chat_id = message.chat.id
    _from = LANGCODES[lang_from]
    _to = LANGCODES[lang_to]

    translated_text = translator.translate(message.text, _to, _from).text

    bot.send_message(chat_id, f'''
FROM: <b>{lang_from}</b>
TO: <b>{lang_to}</b>
ORIGINAL:
<i><b>{message.text}</b></i>
TRANSLATED:
<i><b>{translated_text}</b></i>
''', parse_mode='HTML')
    db.insert_translation(lang_from, lang_to, message.text, translated_text, chat_id)
    command_start(message)


@bot.message_handler(func=lambda msq: msq.text == 'History')
def show_history(message):
    chat_id = message.chat.id
    translations = db.get_user_translations(chat_id)
    print(translations)



























bot.polling(none_stop=True)
