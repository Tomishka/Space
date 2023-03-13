from create_bot import bot
from keyboa import Keyboa           #импорт библиотеки для работы с кнопками
from constants import bot_responses


#доход 0 income
#расход 1 expense
################################################################################
                #level 0
# categories_with_ids = [
#     [{"Расход": "expense"}, {"Доход": "income"}],
#     {"Отмена": "cancel"}
# ]
# categories_text = "Выбери тип для операции:"
#
# expense_with_ids = [
#     {"Транспорт": "transport"}, {"Образование": "edu"},
#     {"Назад": "back"}
# ]
# expense_text = "Выбери цель расхода средств:"
#
# incomes_with_ids = [
#     {"Стипендия": "scholarship"}, {"Зарплата": "salary"},
#     {"Назад": "back"}
# ]
# income_text = "Выбери источник поступления средств:"
################################################################################


categories_with_ids = [
    "Расход", "Доход","Отмена"
]
categories_text = "Выбери тип для операции:"

expense_with_ids = [
    "Транспорт", "Образование","Назад"
]
expense_text = "Выбери цель расхода средств:"

incomes_with_ids = [
    "Стипендия", "Зарплата","Назад"
]
income_text = "Выбери источник поступления средств:"

#вывод кнопки с сообщением о последних доходах?????


def check_level(current_level, message, flag):
    if current_level == 0 and flag == "" :
        button_output(message, categories_with_ids, categories_text) #level0
    elif current_level == 1 and flag == "Доход":
        button_output(message, incomes_with_ids, income_text)
    elif current_level == 1 and flag == "Расход":
        button_output(message, expense_with_ids, expense_text)

@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(chat_id=message.chat.id, text=bot_responses.Welcome)

@bot.message_handler(commands=['help'])
def start_bot(message):
    bot.send_message(chat_id=message.chat.id, text=bot_responses.HelpWords)

@bot.message_handler(commands=['stop'])
def start_bot(message):
    bot.send_message(chat_id=message.chat.id, text=bot_responses.StopWords)

@bot.message_handler(content_types=['text'])
def start(message):
    try:
        int(message.text)
        button_output(message, categories_with_ids, categories_text) #создание кнопок расход/доход
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text=bot_responses.ErrorTypeValue)

@bot.message_handler()
def button_output(message, categories, text):
    keyboard_complex = Keyboa(items=categories)
    bot.send_message(
        chat_id=message.chat.id,
        reply_markup=keyboard_complex(),
        text=text )


@bot.callback_query_handler(func=lambda call:True)
def send_text(call):

    if call.data == "Назад":
        #ничего не делаем, откатываем на уровень назад
        check_level(0, call.message, "")
    elif call.data == "Отмена":
        # ничего не делаем, удаляем все сообщения
        bot.delete_message(call.message.chat.id, call.message.message_id)

    #проверка на попадание в одну из ветвей меню, здесь мы просто смотрим, что выводить дальше
    if call.data == 'Доход':
        check_level(1, call.message, "Доход")
        bot.delete_message(call.message.chat.id, call.message.message_id)  # удаление предыдущего сообщения с кнопками
    elif call.data == 'Расход':
        check_level(1, call.message, "Расход")
        bot.delete_message(call.message.chat.id, call.message.message_id)  # удаление предыдущего сообщения с кнопками

    if call.data in str(expense_with_ids):
        # вызываем метод для добавления строки в бд
        bot.delete_message(call.message.chat.id, call.message.message_id)  # удаление предыдущего сообщения с кнопками
        # сообщение об успешном/не успешном добавлении строки в бд
    elif call.data in str(incomes_with_ids):
        # вызываем метод для добавления строки в бд
        bot.delete_message(call.message.chat.id, call.message.message_id)  # удаление предыдущего сообщения с кнопками
        # сообщение об успешном/не успешном добавлении строки в бд





