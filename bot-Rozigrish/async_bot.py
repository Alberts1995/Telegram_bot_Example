import logging
from aiogram import Bot, Dispatcher, executor, types
from config_r import TOKEN
#from bot_bd import SQLite
from unlocal import MysqlManager
import datetime
from datetime import timedelta
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import requests_async as requests
import asyncio as aio
from aiogram.types import ChatMember, ContentTypes
from aiogram.dispatcher.webhook import SendMessage, get_new_configured_app
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import ssl
import re
from aiohttp import web





API_TOKEN = TOKEN

# WEBHOOK_HOST = 'https://'
# WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
# #WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
# WEBAPP_HOST = 'localhost'
# WEBAPP_PORT = 3001
# WEBHOOK_PATH = f"/{API_TOKEN}"
# BAD_CONTENT = ContentTypes.PHOTO & ContentTypes.DOCUMENT & ContentTypes.STICKER & ContentTypes.AUDIO

# #WEBHOOK_SSL_CERT = 'fullchain1.pem'  # Path to the ssl certificate
# #WEBHOOK_SSL_PRIV = 'privkey1.pem'  # Path to the ssl private key

# #WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL = "{}/{}/".format(WEBHOOK_HOST, API_TOKEN)

# logging.basicConfig(level=logging.INFO)

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot, storage=MemoryStorage())
# dp.middleware.setup(LoggingMiddleware())




db = MysqlManager()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
#db = SQLite()
dp = Dispatcher(bot, storage=MemoryStorage())
new_prank = 'Новый Розыгрыш'
act = 'Активные Розыгрыши'
new = "Добавь меня в администраторы канала и пришли  мне любое сообщение из него"


class GetPlayerState(StatesGroup):
    waiting_for_id = State()
    new_prank_get = State()
    get_info_all = State()
    new_vine = State()
    new_ke = State()
    update_dat = State()
    update_text = State()
    new_text_viner = State()
    get_all_informatio = State()
    Taske = State()


def auth(func):
    async def wrapper(message):
        if int(message.chat.id) in db.select_user():
            await func(message)
        else:
            await message.answer("Вы не зарегистрированы обратитесь к администратору: ")
    return wrapper
    

@dp.message_handler(commands = ["start"])
@auth
async def Task(message): 
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    new_prank = types.KeyboardButton(text = 'Новый Розыгрыш')
    customization = types.KeyboardButton(text = 'Активные Розыгрыши')
    keyboard.add(new_prank, customization)
    await message.answer("Выбери действие", reply_markup = keyboard)

        
@dp.message_handler(lambda message: message.text == new_prank)
@auth
async def del_or_update_managers(message): 
    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    a = []
    for z, v in db.get_chnal().items():
        a.append(types.InlineKeyboardButton(text= z, callback_data= z))
    keyboard.add(*a)
    k = types.InlineKeyboardButton(text="Добавить канал", callback_data='Добавить канал')
    keyboard.add(k)   
    await message.answer("Выбери действие", reply_markup = keyboard)


@dp.message_handler(lambda message: message.text == act)
@auth
async def act_tas(message): 
    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    ke = (types.InlineKeyboardButton(text= "Закончить досрочно", callback_data= "Закончить досрочно"))
    keyboard.add(ke)
    for z in db.act_task():    
        await message.answer(f"Название канала/чата: {z[7]}\nВремя кокнчания: {z[4]}\nТекст: {z[2]}\nПобедитель: {z[8]}", reply_markup = keyboard) 


@dp.message_handler(state=GetPlayerState.waiting_for_id)
async def seave_new_prank(message: types.Message, state: FSMContext):
    try:
        if [i for i in db.get_time() if i[1] == str(message.forward_from_chat.id)]:
            await state.finish()
            await message.answer("Канал уже существует")
            await Task(message)
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            back = types.KeyboardButton(text = 'Отмена')
            db.insert_new(message.forward_from_chat.id, message.forward_from_chat.title, message.chat.id)
            keyboard.add(back)
            await message.answer("Пришли мне текст для розыгрыша", reply_markup = keyboard)
            await state.finish()
            await GetPlayerState.new_prank_get.set()
    except AttributeError:
        if message.text == "Отмена":
            await state.finish()
            await Task(message)
        else:
            await state.finish()
            await message.answer("Неверный формат данных")
            await Task(message)



async def get_all_information_on_prank(message):
    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    men = db.get_info(message.chat.id)
    k = types.InlineKeyboardButton(text="Назначить победителя", callback_data='Назначить победителя')
    k1 = types.InlineKeyboardButton(text="Поменять текст кнопки", callback_data='Поменять текст кнопки')
    k2 = types.InlineKeyboardButton(text="Смена чат/канала", callback_data='Смена чат/канала')
    k3 = types.InlineKeyboardButton(text="Смена Времени окончания", callback_data='Смена Времени окончания')
    k4 = types.InlineKeyboardButton(text="Изменить Текст", callback_data='Изменить Текст')
    k5 = types.InlineKeyboardButton(text="Изменить Текст Победителя", callback_data='Изменить Текст Победителя')
    k6 = types.InlineKeyboardButton(text="Готово", callback_data='Готово')
    keyboard.add(k, k1, k2, k3, k4, k5)
    keyboard.add(k6)
    await message.answer(f"Что вы хотите изменить в розыгрыше?\nВермя окончания: {men[0][4]}\nКанал/Чат: {men[0][7]}\nТекст: {men[0][2]}\nПобидителей: {men[0][8]}\nТекст кнопки: {men[0][9]}\nТекст для победителя: {men[0][3]}", reply_markup = keyboard)


@dp.callback_query_handler(lambda call: True)
async def callback(call):
    if call.data == "Добавить канал":
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        back = types.KeyboardButton(text = 'Отмена')
        keyboard.add(back)
        await bot.send_message(call.from_user.id, f"{new}", reply_markup=keyboard)
        await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        await GetPlayerState.waiting_for_id.set()
    elif call.data == "Назначить победителя":
        await bot.send_message(chat_id = call.message.chat.id, text = "Напиши Имя пользователя\nНапример: @ivanov")
        await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        await GetPlayerState.new_vine.set()
    elif call.data == "Поменять текст кнопки":
        await bot.send_message(chat_id = call.message.chat.id, text = "Текст Кнопки")
        await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        await GetPlayerState.new_ke.set()
    elif call.data == "Смена Времени окончания":
        date = datetime.datetime.now() + timedelta(minutes=60)
        await bot.send_message(chat_id = call.message.chat.id, text = f"Введите Новую Дату или время\nНапример: {date}")
        await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        await GetPlayerState.update_dat.set()
    elif call.data == "Изменить Текст":
        await bot.send_message(chat_id = call.message.chat.id, text = "Введите Новый Текст")
        await GetPlayerState.update_text.set()
    elif call.data == "Изменить Текст Победителя":
        await bot.send_message(chat_id = call.message.chat.id, text = "Напиши новое сообщение победителю\nНапример: В данном розыгрыше стал победителем:")
        await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        await GetPlayerState.new_text_viner.set()
    elif call.data == "Закончить досрочно":
        for z in db.act_task():
            if z[7] == call.message.text.split("\n")[0][22:]:
                url = f'https://api.telegram.org/bot{TOKEN}/deleteMessage?chat_id={z[1]}&message_id={z[5]}'
                await requests.get(url)
                db.inser_status(z[5])
                db.delet_draw(z[5])
        await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
    elif call.data == "Смена чат/канала":
        keyboard = types.InlineKeyboardMarkup(row_width = 2)
        a = []
        for z, v in db.get_chnal_two().items():
            a.append(types.InlineKeyboardButton(text= z, callback_data= z))
        keyboard.add(*a)
        if a == []:
            await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
            await bot.send_message(chat_id = call.message.chat.id, text = "Нету свободных каналов", reply_markup=keyboard)
            await get_all_informatio(call.message, FSMContext)
        else:
            await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
            await bot.send_message(chat_id = call.message.chat.id, text = "Выберите Канал", reply_markup=keyboard)
    elif call.data == "Готово":
        try:
            keyboard = types.InlineKeyboardMarkup()
            mes = db.get_chnal_and_text(call['from'].id)
            ke = types.InlineKeyboardButton(text= mes[0][-2], callback_data= mes[0][-2])
            keyboard.add(ke)
            x = await bot.send_message(chat_id = mes[0][1],  text = mes[0][2], reply_markup= keyboard)
            db.inser_status_message_id(x['message_id'], call['from'].id)
            await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
            await Task(call.message)
        except Exception:
            await bot.send_message(chat_id = call.message.chat.id, text =  "Не являюсь администратором какнала/чата либо нет такого канала/чата")
    elif call.data in db.get_chnal_two():
        ids = str(call['from'].id)
        db.inser_status_new(db.get_chnal_three()[ids])
        db.update_chanal(call.data, db.get_chnal_two(), call['from'].id)
        db.inser_status_new(call)
        await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
        await get_all_informatio(call.message, FSMContext)
    elif call.data in db.get_chnal():
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        back = types.KeyboardButton(text = 'Отмена')
        keyboard.add(back)
        for x, y in db.get_chnal().items():
            if call.data == x:
                db.new_update_chanal(x.split(" ")[2], call['from'].id)
                await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
                await get_all_informatio(call.message, FSMContext)
    elif call.data == db.get_chnal_and_text_new(call.message.message_id)[0][-2]:
        req = await bot.get_chat_member(chat_id = call.message.chat.id, user_id = call.from_user.id)
        if req['status'] == "member" or  req['status'] == "creator":
            g = req['user']['id'], '@' + req['user']['username'], call.message.message_id, f"{call.message.chat.id}"
            if db.select_info(call.message.chat.id) == 0:
                db.inser_user_new_draw(req['user']['id'], req['user']['username'], call.message.message_id, call.message.chat.id)
                await bot.answer_callback_query(callback_query_id=call.id, text="Теперь вы участвуете в розыгрыше", show_alert=False)
            elif g in db.select_info(call.message.chat.id):
                await bot.answer_callback_query(callback_query_id=call.id, text="Вы уже зарегестрированы", show_alert=False)    
            else:
                db.inser_user_new_draw(req['user']['id'], req['user']['username'], call.message.message_id, call.message.chat.id)
                await bot.answer_callback_query(callback_query_id=call.id, text="Теперь вы участвуете в розыгрыше", show_alert=False)
        elif req['status'] == "left":
            await bot.answer_callback_query(callback_query_id=call.id, text="Вы не подписаны на канал", show_alert=False)





@dp.message_handler(state=GetPlayerState.new_prank_get)
async def get_new_prank(message: types.Message, state: FSMContext): 
    if message.text == "Отмена":
        db.delet_informations(message.chat.id)
        await state.finish()
        await Task(message)
    else:
        date = datetime.datetime.now() + timedelta(minutes=60)
        db.inser_text(message.text, date, message.chat.id)
        await state.finish()
        await get_all_information_on_prank(message)

@dp.message_handler(state=GetPlayerState.new_vine)
async def new_viner(message: types.Message, state: FSMContext):
    db.new_viner(message.text, message.chat.id)
    await state.finish()
    await get_all_information_on_prank(message)

@dp.message_handler(state=GetPlayerState.new_ke)
async def new_key(message: types.Message, state: FSMContext):
    db.inser_text_key(message.text, message.chat.id)
    await state.finish()
    await get_all_information_on_prank(message)

@dp.message_handler(state=GetPlayerState.update_dat)
async def update_data(message: types.Message, state: FSMContext):
    db.update_data(message.text, message.chat.id)
    await state.finish()
    await get_all_information_on_prank(message)

@dp.message_handler(state=GetPlayerState.update_text)
async def update_text(message: types.Message, state: FSMContext):
    db.update_text(message.text, message.chat.id)
    await state.finish()
    await get_all_information_on_prank(message)

@dp.message_handler(state=GetPlayerState.new_text_viner)
async def new_text_viner(message: types.Message, state: FSMContext):
    db.new_text_viner(message.text, message.chat.id)
    await state.finish()
    await get_all_information_on_prank(message)


@dp.message_handler(state=GetPlayerState.get_all_informatio)
async def get_all_informatio(message: types.Message, state: FSMContext):
    #await state.finish()
    await get_all_information_on_prank(message)


@dp.message_handler(state=GetPlayerState.Taske)
async def Taske(message: types.Message, state: FSMContext):
    await state.finish()
    await Task(message)


@dp.message_handler(lambda message: message.text == "Отмена")
async def cancel(message: types.Message): 
    db.delet_informations(message.chat.id)
    await Task(message)



if __name__ == "__main__":
    executor.start_polling(dp, timeout=500, relax=0.01)
    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )