import config
import telebot
import time
from telebot import types
from Task_manager_bd import SQLite
import datetime


bd = SQLite()
bot = telebot.TeleBot(config.token)
new = 'Новое задание'
information_task = 'Список заданий'
back = "Назад"
#name_all_manager = {"Aleksander":"959836209", "Anya":"680497281", "Artem":"821702226", "Pasha":"1297163437", "Dasha":"702012759", "Ruslana": "349943091"}
#name_manager = {"Саша":"959836209", "Аня":"680497281", "Артем":"821702226", "Паша":"1297163437", "Даша":"702012759", "Руслана": "349943091"}
all_history = "Вся История Задач"
times = {"10 мин": 600, "30 мин": 1800, "60 мин": 3600}
update_or_delet = "Удалить/Добавить участника"
udpate_manager = "Добавить участника"
delet_manager = "Удалить учатника"
global text
text = " "

# Выбор всех действий
@bot.message_handler(commands = ["start"])
def Task(message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    new = telebot.types.KeyboardButton(text = 'Новое задание')
    all_task = telebot.types.KeyboardButton(text = 'Список заданий')
    history = telebot.types.KeyboardButton(text = 'Вся История Задач')
    del_or_update_manager = telebot.types.KeyboardButton(text = 'Удалить/Добавить участника')
    keyboard.add(new, all_task, history, del_or_update_manager)
    bot.send_message(message.chat.id, "Выбери действие", reply_markup = keyboard)

# Выбрано Удалить/Добавить участника
@bot.message_handler(func=lambda m: m.text == update_or_delet)
def del_or_update_managers(message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    back = telebot.types.KeyboardButton(text = 'Назад')
    delete = telebot.types.KeyboardButton(text = 'Удалить учатника')
    update = telebot.types.KeyboardButton(text = 'Добавить участника')
    keyboard.add(delete, update)
    keyboard.add(back)
    bot.send_message(message.chat.id, "Выберите Действие", reply_markup=keyboard)


# Выбрано Добавить участника
@bot.message_handler(func=lambda m: m.text == udpate_manager)
def udpdate_managers(message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    back = telebot.types.KeyboardButton(text = 'Назад')
    keyboard.add(back)
    send = bot.send_message(message.chat.id, "Введите имя и chat_id\nНапример:\nВаня\n123456799", reply_markup=keyboard)
    bot.register_next_step_handler(send, print_message)
    

# Выбрано Удалить участника
@bot.message_handler(func=lambda m: m.text == delet_manager)
def delet_managers(message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    a = []
    back = telebot.types.KeyboardButton(text = 'Назад')
    for z, v in bd.select_for_buttom().items(): # вызов из бд имен которые будут в виде кнопки
        a.append(telebot.types.KeyboardButton(text = z))
    keyboard.add(*a)
    keyboard.add(back)
    send = bot.send_message(message.chat.id, "Выберите кого хотите удалить", reply_markup=keyboard)
    bot.register_next_step_handler(send, del_man_sql)


# Выбрано Новое задание
@bot.message_handler(func=lambda m: m.text == new)
def who_is(message: types.Message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    a = []
    back = telebot.types.KeyboardButton(text = 'Назад')
    for z, v in bd.select_for_buttom().items(): # вызов из бд имен которые будут в виде кнопки
        a.append(telebot.types.KeyboardButton(text = z))
    keyboard.add(*a)
    keyboard.add(back)
    send = bot.send_message(message.chat.id, "Выберите Участника", reply_markup=keyboard)
    bot.register_next_step_handler(send, process_new_task)
    

# Запись нового задания
def process_new_task(message: types.Message): 
    if message.text == "Назад":
        Task(message)
    else:
        chat_id = bd.select_for_buttom() # вызов из бд имен которые будут в виде кнопки
        bd.chat_id_and_status(datetime.date.today(), message.text, chat_id[message.text]) # запись в бд данных
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True)
        back = telebot.types.KeyboardButton(text = 'Отменить')
        keyboard.add(back)
        send = bot.send_message(message.chat.id, "Напиши новое задание", reply_markup=keyboard)
        bot.register_next_step_handler(send, get_new_task)


# Вывод времени 
def process_time(message: types.Message):
    message_body = bd.select_all()
    keyboard = types.InlineKeyboardMarkup(row_width = 3)
    a = []
    for z in times:
        a.append(types.InlineKeyboardButton(text= z, callback_data= times[z]))
    keyboard.add(*a)   
    bot.send_message(message.chat.id, f'Задание: {message_body[0]}\nИмя: {message_body[6]}\nЗадание: {message_body[3]}\n\nВыбери временные рамки', reply_markup=keyboard)

# работа с инлайн кнопками
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data in ['600', '1800', '3600']:
        bd.sleep(call.data)
        message_body = bd.select_all()
        keyboard = types.InlineKeyboardMarkup(row_width = 1)
        k1 = types.InlineKeyboardButton(text="Готово!", callback_data='ready')
        keyboard.add(k1)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text =  f'Задание: {message_body[0]}\nИмя: {message_body[6]}\nЗадание: {message_body[3]}\nВремя {message_body[4]//60} мин', reply_markup=keyboard)
    elif call.data=="ready":
        Task(call.message)       
    elif call.data == "Завершить":
        bd.deactivate_task(int(call.message.text.split("\n")[0].split(" ")[-1]))
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
    elif call.data == "Изменить":
        keyboard = types.InlineKeyboardMarkup(row_width = 2)
        k1 = types.InlineKeyboardButton(text="Текст задачи", callback_data='Текст задачи')
        k2 = types.InlineKeyboardButton(text="Исполнитель", callback_data='Исполнитель')
        k3 = types.InlineKeyboardButton(text="Частота уведомления", callback_data='Частота уведомления')
        keyboard.add(k1, k2, k3)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = call.message.text, reply_markup=keyboard)
    elif call.data == "Исполнитель":
        keyboard = types.InlineKeyboardMarkup(row_width = 2)
        a = []
        for z, v in bd.select_for_buttom().items():
            a.append(types.InlineKeyboardButton(text= z, callback_data= z))
        keyboard.add(*a)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = call.message.text, reply_markup=keyboard)
    elif call.data in bd.select_for_buttom():
        chat_id = bd.select_for_buttom()
        #print(int(call.message.text.split("\n")[0].split(" ")[-1]), call.data, name_all_manager[call.data])
        bd.update_manager(int(call.message.text.split("\n")[0].split(" ")[-1]), call.data, chat_id[call.data])
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
    elif call.data == "Частота уведомления":
        keyboard = types.InlineKeyboardMarkup(row_width = 3)
        a = []
        for z in times:
            a.append(types.InlineKeyboardButton(text= z, callback_data= z))
        keyboard.add(*a)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = call.message.text, reply_markup=keyboard)
    elif call.data in times:
        bd.update_sleep(int(times[call.data]), call.message.text.split("\n")[0].split(" ")[-1])
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
    elif call.data == "Текст задачи":
        global text
        text = int(call.message.text.split("\n")[0].split(" ")[-1])
        keyboard = types.ReplyKeyboardMarkup(True)
        keyboard.add(types.KeyboardButton(text = 'Назад'))
        send = bot.send_message(chat_id = call.message.chat.id, text = "Введите текст задачи", reply_markup=keyboard)
        bot.register_next_step_handler(send, remake_task)


def remake_task(message):
    global text
    if message.text=='Назад':
        process_back(message)
    else:
        bd.update_task(int(text), message.text)
        who_is(message)


# Выбрано Список заданий
@bot.message_handler(func=lambda m: m.text == information_task)
def process_information_all_task(message: types.Message): 
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    a = []
    back = telebot.types.KeyboardButton(text = 'Назад')
    for z, v in bd.select_for_buttom().items(): # вызов из бд имен которые будут в виде кнопки
        a.append(telebot.types.KeyboardButton(text = z))
    keyboard.add(*a)
    keyboard.add(back)
    send = bot.send_message(message.chat.id, "Выберите участника", reply_markup=keyboard)
    bot.register_next_step_handler(send, process_information_task)


# Выбор человека из спика которому нужно что либо поменять
def process_information_task(message: types.Message):
    if message.text == "Назад":
        Task(message)
    else:
        chat_id = bd.select_for_buttom()
        message_body = bd.select_manager(int(chat_id[message.text])) # отселживаю  по chat_id
        for x in range(len(message_body)):
            keyboard = types.InlineKeyboardMarkup(row_width = 2)
            k1 = types.InlineKeyboardButton(text="Завершить", callback_data='Завершить')
            k2 = types.InlineKeyboardButton(text="Изменить", callback_data='Изменить')
            keyboard.add(k1, k2)
            bot.send_message(message.chat.id, f'Задание: {message_body[x][0]}\nИмя: {message_body[x][6]}\nЗадание: {message_body[x][3]}\nЧастота уведомления: {message_body[x][4]//60} мин\nДата создание задачи: {message_body[x][5]}', reply_markup=keyboard)
        process_information_all_task(message)

# Вся история
@bot.message_handler(func=lambda m: m.text == all_history)
def history_task(message: types.Message): 
    message_body = bd.select_manager_task_all() # Смотреть из базы все дейстивя
    for x, y in enumerate(message_body):
        if message_body[x][3] == None:
            pass
        else:
            bot.send_message(message.chat.id, f'Задание: {message_body[x][0]}\nИмя: {message_body[x][6]}\nЗадание: {message_body[x][3]}\nДата создание задачи: {message_body[x][5]}')

# При условии что нажали отмена
@bot.message_handler(func=lambda m: m.text == "Отменить")
def cancel(message): 
    bd.deactivate()
    Task(message)


# Запись задания 
def get_new_task(message): 
    if message.text == "Отменить":
        cancel(message)
    else:
        bd.new_task(message.text)
        process_time(message)

# При условии что нажали Назад
@bot.message_handler(func=lambda m: m.text == "Назад")
def process_back(message): 
    Task(message)

# Создание нового человека
def print_message(message):
    bd.new_manager(message.text.split("\n")[0], message.text.split("\n")[1])
    Task(message)

# Удалить человека 
def del_man_sql(message):
    bd.deactivate_managers(message.text)
    Task(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)