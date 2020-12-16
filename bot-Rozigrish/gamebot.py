import telebot
from bot_bd import SQLite
from telebot import types
import datetime
from datetime import timedelta
import requests
from config_r import TOKEN
import logging

db = SQLite()
bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
new_prank = 'Новый Розыгрыш'
act = 'Активные Розыгрыши'


global new_people
new_people = []

# Выбор всех действий
@bot.message_handler(commands = ["start"])
def Task(message):
    if int(message.chat.id) in db.select_user():
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        new_prank = telebot.types.KeyboardButton(text = 'Новый Розыгрыш')
        customization = telebot.types.KeyboardButton(text = 'Активные Розыгрыши')
        keyboard.add(new_prank, customization)
        bot.send_message(message.chat.id, "Выбери действие", reply_markup = keyboard)
    else:
        bot.send_message(message.chat.id, "Вы не зарегистрированы обратитесь к администратору: @CPA_1_Admin")


@bot.message_handler(func=lambda m: m.text == new_prank)
def del_or_update_managers(message): 
    if int(message.chat.id) in db.select_user():
        keyboard = types.InlineKeyboardMarkup(row_width = 2)
        a = []
        for z, v in db.get_chnal().items():
            a.append(types.InlineKeyboardButton(text= z, callback_data= z))
        keyboard.add(*a)
        k = types.InlineKeyboardButton(text="Добавить канал", callback_data='Добавить канал')
        keyboard.add(k)   
        bot.send_message(message.chat.id, "Выбери канал", reply_markup = keyboard)
    else:
        bot.send_message(message.chat.id, "Вы не зарегистрированы обратитесь к администратору: @CPA_1_Admin")


@bot.message_handler(func=lambda m: m.text == act)
def act_tas(message): 
    if int(message.chat.id) in db.select_user():
        keyboard = types.InlineKeyboardMarkup(row_width = 2)
        ke = (types.InlineKeyboardButton(text= "Закончить досрочно", callback_data= "Закончить досрочно"))
        keyboard.add(ke)
        for z in db.act_task():    
            bot.send_message(message.chat.id, f"Название канала/чата: {z[7]}\nВремя кокнчания: {z[4][0:19]}\nТекст: {z[2]}\nПобедитель: {z[8]}", reply_markup = keyboard) 
    else:
        bot.send_message(message.chat.id, "Вы не зарегистрированы обратитесь к администратору: @CPA_1_Admin")


def seave_new_prank(message):
    if message.text == "Отмена":
        Task(message)
    elif [i for i in db.get_time() if i[1] == str(message.forward_from_chat.id)]:
        send = bot.send_message(message.chat.id, "Канал уже существует")
        Task(message)
    else:
        try:
            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            back = telebot.types.KeyboardButton(text = 'Отмена')
            db.insert_new(message.forward_from_chat.id, message.forward_from_chat.title)
            keyboard.add(back)
            send = bot.send_message(message.chat.id, "Пришли мне текст для розыгрыша", reply_markup = keyboard)
            bot.register_next_step_handler(send, get_new_prank)
        except AttributeError:
            send = bot.send_message(message.chat.id, "Неверный формат данных", reply_markup = keyboard)
            bot.register_next_step_handler(send, seave_new_prank)



def get_all_information_on_prank(message):
    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    men = db.get_info()
    k = types.InlineKeyboardButton(text="Назначить победителя", callback_data='Назначить победителя')
    k1 = types.InlineKeyboardButton(text="Поменять текст кнопки", callback_data='Поменять текст кнопки')
    k2 = types.InlineKeyboardButton(text="Смена чат/канала", callback_data='Смена чат/канала')
    k3 = types.InlineKeyboardButton(text="Смена Времени окончания", callback_data='Смена Времени окончания')
    k4 = types.InlineKeyboardButton(text="Изменить Текст", callback_data='Изменить Текст')
    k5 = types.InlineKeyboardButton(text="Изменить Текст Победителя", callback_data='Изменить Текст Победителя')
    k6 = types.InlineKeyboardButton(text="Готово", callback_data='Готово')
    keyboard.add(k, k1, k2, k3, k4, k5)
    keyboard.add(k6)
    bot.send_message(message.chat.id, f"Что вы хотите изменить в розыгрыше?\nВермя окончания: {men[0][4][0:19]}\nКанал/Чат: {men[0][7]}\nТекст: {men[0][2]}\nПобидителей: {men[0][8]}\nТекст кнопки: {men[0][9]}\nТекст для победителя: {men[0][3]}", reply_markup = keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "Смена чат/канала":
        keyboard = types.InlineKeyboardMarkup(row_width = 2)
        a = []
        for z, v in db.get_chnal_two().items():
            a.append(types.InlineKeyboardButton(text= z, callback_data= z))
        keyboard.add(*a)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Выберите Канал", reply_markup=keyboard)
    elif call.data in db.get_chnal_two():
        db.update_chanal(call.data, db.get_chnal_two()[call.data])
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        get_all_information_on_prank(call.message)
    elif call.data == "Изменить Текст":
        send = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите Новый Текст")
        bot.register_next_step_handler(send, update_text)
    elif call.data == "Смена Времени окончания":
        send = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Введите Новую Дату или время\nНапример: 2020-10-30 12:51:36")
        bot.register_next_step_handler(send, update_data)
    elif call.data == "Добавить канал":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        back = telebot.types.KeyboardButton(text = 'Отмена')
        keyboard.add(back)
        send = bot.send_message(chat_id = call.message.chat.id, text = "Добавь меня в администраторы канала и пришли  мне любое сообщение из него", reply_markup=keyboard)
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(send, seave_new_prank)
    elif call.data == "Готово":
        try:
            keyboard = types.InlineKeyboardMarkup()
            mes = db.get_chnal_and_text()
            ke = types.InlineKeyboardButton(text= mes[0][-1], callback_data= mes[0][-1])
            keyboard.add(ke)
            print(bot.send_message(chat_id = mes[0][1],  text = mes[0][2], reply_markup= keyboard))
            bot.send_message(chat_id = mes[0][1],  text = mes[0][2], reply_markup= keyboard)
            bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
            Task(call.message)
        except Exception:
            bot.send_message(chat_id = call.message.chat.id, text =  "Не являюсь администратором какнала/чата либо нет такого канала/чата")
    elif call.data == db.get_chnal_and_text()[0][-1]:
        url = f'https://api.telegram.org/bot1476829170:AAGiOgA0R64w3qR9ID-ESH7wrHB8B8GXEM4/getChatMember?chat_id={call.message.chat.id}&user_id={call.from_user.id}'
        req = requests.get(url).json()
        if req['result']['status'] == "member" or  req['result']['status'] == "creator":
            g = req['result']['user']['id'], '@' + req['result']['user']['username'], call.message.message_id, f"{call.message.chat.id}"
            global new_people

            print(req['result']['user']['id'], req['result']['user']['username'], call.message.message_id, call.message.chat.id)
            bot.answer_callback_query(callback_query_id=call.id, text="Теперь вы участвуете в розыгрыше", show_alert=False, cache_time = 0.1)
            if db.select_info(call.message.chat.id) == 0:
                db.inser_status_message_id(call.message.message_id)
                db.inser_user_new_draw(req['result']['user']['id'], req['result']['user']['username'], call.message.message_id, call.message.chat.id)
                bot.answer_callback_query(callback_query_id=call.id, text="Теперь вы участвуете в розыгрыше", show_alert=False)
            elif g in db.select_info(call.message.chat.id):
                bot.answer_callback_query(callback_query_id=call.id, text="Вы уже зарегестрированы", show_alert=False)    
            else:        
                db.inser_status_message_id(call.message.message_id)
                db.inser_user_new_draw(req['result']['user']['id'], req['result']['user']['username'], call.message.message_id, call.message.chat.id)
                bot.answer_callback_query(callback_query_id=call.id, text="Теперь вы участвуете в розыгрыше", show_alert=False)
        elif req['result']['status'] == "left":
            bot.answer_callback_query(callback_query_id=call.id, text="Вы не подписаны на канал", show_alert=False)
    elif call.data == "Поменять текст кнопки":
        send = bot.send_message(chat_id = call.message.chat.id, text = "Текст Кнопки")
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(send, new_key)
    elif call.data == "Назначить победителя":
        send = bot.send_message(chat_id = call.message.chat.id, text = "Напиши Имя пользователя\nНапример: @ivanov")
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(send, new_viner)
    elif call.data == "Закончить досрочно":
        for z in db.act_task():
            if z[7] == call.message.text.split("\n")[0][22:]:
                db.inser_status(z[5])
                db.delet_draw(z[5])
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
    elif call.data in db.get_chnal():
        for x, y in db.get_chnal().items():
            if call.data == x:
                db.inser_chat_id(db.sel(y)[0][1], db.sel(y)[0][2], db.sel(y)[0][3], db.sel(y)[0][4], db.sel(y)[0][5], db.sel(y)[0][6], db.sel(y)[0][7], db.sel(y)[0][8], db.sel(y)[0][9])
                db.delet_chanal(db.sel(y)[0][0])
                bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
                get_all_information_on_prank(call.message)
    elif call.data == "Изменить Текст Победителя":
        send = bot.send_message(chat_id = call.message.chat.id, text = "Напиши новое сообщение победителю\nНапример: В данном розыгрыше стал победителем:")
        bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(send, new_text_viner)


def update_text(message):
    db.update_text(message.text)
    get_all_information_on_prank(message)


def update_data(message):
    db.update_data(message.text + ".997267")
    get_all_information_on_prank(message)


def new_key(message):
    db.inser_text_key(message.text)
    get_all_information_on_prank(message)


def new_viner(message):
    db.new_viner(message.text)
    get_all_information_on_prank(message)


def new_text_viner(message):
    db.new_text_viner(message.text)
    get_all_information_on_prank(message)


def get_new_prank(message): 
    if message.text == "Отмена":
        db.delet_informations()
        Task(message)
    else:
        date = datetime.datetime.now() + timedelta(minutes=60)
        db.inser_text(message.text, date)
        get_all_information_on_prank(message)


@bot.message_handler(func=lambda m: m.text == "Отмена")
def cancel(message: types.Message): 
    db.delet_informations()
    Task(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=1)