import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6682285702:AAG-LCHg1XtJo4cYo0aNZDF_L2O3NRXvpHU",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()
    tayn = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Супер Мега Важный опрос"
text_button_1 = "Что вообще такое Питон?"
text_button_2 = "10 интересных фактов про Python"
text_button_3 = "Самые популярные языки программирования :)"
text_button_4 = "Лучшая онлаин школа :)"

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    ),
    telebot.types.KeyboardButton(
        text_button_4,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        '*Привет!* Я твой личный бот. Я помогу тебе поближе познакомиться и изучить Python! Но для начала пройди *опрос.*',
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! Напиши пж своё _имя_? :)')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Молодец! А теперь введи свой Возраст.')
    bot.set_state(message.from_user.id, PollState.tayn, message.chat.id)


@bot.message_handler(state=PollState.tayn)
def tayn(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['tayn'] = message.text
    bot.send_message(message.chat.id,
                     'А ты знал определение что такое [возраст](https://ru.wikipedia.org/wiki/Возраст) :)')
    bot.send_message(message.chat.id,
                     'Круто! Остался последний шаг: введите свой [город](https://ru.wikipedia.org/wiki/Город)')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id,
                     'Спасибо что прошел важный для меня опрос! Теперь ты можешь по изучать любимый Питончик)))',
                     reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "(https://ru.wikipedia.org/wiki/Python)", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "(https://xakep.ru/2017/08/22/geekbrains-python-promo/)",
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "(https://cf3.ppt-online.org/files3/slide/z/ZTicKN18bXJrGxyHlMSEhVU74nkmgOqeRFW6YB/slide-3.jpg)",
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_4 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "(https://umschool.net/)", reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()