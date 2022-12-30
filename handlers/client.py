import copy
import os
import time
from datetime import datetime
from sqlite3 import OperationalError
from DB_Load_Photo import *
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import zz_zayav, kb_contact
from keyboards import kb_client_menu2, AdminPanell  #kb_client_proch,
from excel_loader import edit2
from kbs import add_button_menu, del_button_new, get_menu
from dinamic_kbs import dinamic_kbs
from client_commands import get_commands_client
from excel_loader import phone_number
from UrlRefer.generateDB import mail_info_refer
from data_base.sqlite_db import more_media, photo_categ
import sqlite3 as sq
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards import button_case_admin2, cancel_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton


menu = get_menu()

# список кому доступна кнопка вывод excel file
excel_files = ['5295520075']
msg_id_bot = []
msg_id_user = []

# dinamic keyboards
arr = []

# Активное меню для добавления кнопки
active_dinamic_menu = None

# Состояние
# 0 - по умолчанию
# 1 - добавление кнопки
# 2 - удаление кнопки
is_state_button = [0]  # для того чтобы узнать в каком разделе мы находимся, чтобы именно туда добавить кнопку


cur = []
# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):

    global is_state_button, admin_dict
    is_state_button = [0]

    global msgBot
    global arr, cur


    # проверка на рефера
    if len(message.text) > 6:  # проверка есть ли код рефера, если больше 6-ти, значит та что-то помимо /start
        try:
            code = message.text.split(" ")[1]  # берем уникальный код из реф ссылки
            res = mail_info_refer(code)
            cur.append(res)
            # url_bot = cur[0][4]
            # user_id = cur[0][0]
            # user_name = cur[0][1]
            # url_user = cur[0][2]
            # code = cur[0][3]

            # print()
        except IndexError as ex:
            print(ex)


    msg_id_user.clear()
    msgUser = message  # берем id msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)

    # Определяем и добавляем кнопку "Добавить кнопку", если админ
    admin_dict = await bot.get_chat_administrators(chat_id='-1001854126142')  # получаем админов группы  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    arr = dinamic_kbs(admin_group(message.chat.id, admin_dict))  # str(message['from']['id']) in excel_files
    try:
        # кнопка вывести файл будет доступна только определенным людям
        # if str(message.from_user.id) in excel_files:
        if admin_group(message.chat.id, admin_dict):
            msgBot = await message.answer("Вас приветствует\nЧат-бот \"Управление туризмом\"\n\nЕсли вы зашли не в тот пункт меню,\n и нужно вернуться назад,\nнапишите: /start\n\n"
                             "Если уже начали оформлять заявку\n и что-то ввели не верно,\nнапишите слово: *отмена*", parse_mode= "Markdown", reply_markup=AdminPanell)
            msg_id_bot.append(msgBot)
        else:
            msgBot = await message.answer("Вас приветствует\nЧат-бот \"Управление туризмом\"\n\nЕсли вы зашли не в тот пункт меню,\n и нужно вернуться назад,\nнапишите: /start\n\n"
                "Если уже начали оформлять заявку\n и что-то ввели не верно,\nнапишите слово: *отмена*",
                parse_mode="Markdown", reply_markup=zz_zayav)
            msg_id_bot.append(msgBot)
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \nhttps://t.me/tourism_management_bot')  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# @dp.message_handler(commands=[''Вывести_файл''])
async def file_excel_loader(message : types.Message):
    global msgBot
    'для отправки файла excel'
    msgUser = message  # берем msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)
    admin_dict = await bot.get_chat_administrators(chat_id='-1001854126142')  # получаем админов группы  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    if admin_group(message.chat.id, admin_dict):  # файл могут получить админы группы
        try:
            await message.reply_document(open('my_book.xlsx', 'rb'), reply_markup=AdminPanell)
        except FileNotFoundError as ex:
            await bot.send_message(message.chat.id, "Файл еще не создан!")

    try:
        for i in msg_id_user:  # удаляем все сообщения от бота
            await i.delete()
        msg_id_user.clear()  # очищаем словарь, чтобы не возникали ошибки, или не перебрасывало в except, когда это не нужно
    except:
        await msgUser.delete()

    # for i in msg_id_bot:  # очищаем список
    #     msg_id_user.remove(i)

    # for i in msg_id:
    #     await i.delete()  # удаляем смс бота
    # await msgs.delete()  # удаляем смс бота

commands_data = []  # формируем под категории
# @dp.message_handler(commands=['Заполнить_заявку'])
async def otkr_menu(message : types.Message):
    global commands_data

    for option in menu:  # для формирования команд из кнопок

        for keyboard in option['keyboards']:

            _handler = keyboard['handler']

            if _handler == 'dat_ukaz':

                for button in keyboard['buttons']:
                    commands_data.append(button['text'])


    global phone_contact, admin_dict
    global active_dinamic_menu
    me = await bot.get_me()  # получить информацию о боте
    # print(me)
    # print(message.from_user.id, "********")
    # print(message.from_user.username)
    # print(message.chat.id)
    admin_dict = await bot.get_chat_administrators(chat_id='-1001854126142')  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    from lists_news import greeting

    data = datetime.now().strftime("%d_%m_%Y").split("_")[1]

    # преверяем сохранили ли мы номер месяца в документ
    check_file = os.path.exists('number_month.txt')
    if check_file: # если да, берем оттуда дату и сравниваем с актуальной датой
        with open('number_month.txt', 'r', encoding='utf-8') as file:
            file = file.read()
            # print(file, "file")
            # print(data, "data")
            if file != data:  # если даты разные новый лист создается, а если одинаковые не создает, тс мы такое развитие просто пропускаем
                greeting()
                with open('number_month.txt', 'w', encoding='utf-8') as file:  # обновляем дату
                    file.write(str(data))
    else:  # если нет, создаем новый
        with open('number_month.txt', 'w', encoding='utf-8') as file:  # сохраняем туда дату
            file.write(str(data))
        greeting()  # и создаем новый лист

     # если совпали, значит тот же день, и нет нужды в создании нового листа
    name_sud_vrem.clear() # чистим список, чтобы при повторном зявке не было так как будно он выбрал море
    msgUser = message  # берем msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)
    phone_contact = await phone_number(message.chat.id)  # чтобы не переспрашивать номер
    # print(phone_contact, "phone_contact")
    if phone_contact:  # номер есть, поэтому сразу открываем ему главное меню
        if edit2['is'] == 0:
            active_dinamic_menu = 'kb_client_menu'
            msgBot = await bot.send_message(message.chat.id, 'Меню', reply_markup=arr['kb_client_menu'])
            msg_id_bot.append(msgBot)
            # print(msg_id)
        else:
            msgBot = await bot.send_message(message.chat.id, 'Меню', reply_markup=kb_client_menu2)
            msg_id_bot.append(msgBot)
            # print(msg_id)
        phonenumber= str(phone_contact)
        # для вывода в тг создаем список
        sp_phone[message.chat.id] = phonenumber
    else:
        msgBot = await message.answer("Поделитесь номером телефона", reply_markup=kb_contact)
        msg_id_bot.append(msgBot)

def admin_group(user_id, admin):
    """Проверяем админ ли группы"""
    admin_group = {}
    for i in admin:
        admin_group[i["user"]["id"]] = i["status"]
    try:
        if admin_group[user_id] == 'creator' or admin_group[user_id] == 'administrator':
            return True
    except KeyError:
        return False


sp_phone = {}
# перехватываем номер телефона
# @dp.message_handler(content_types=['contact'])
async def contact(message):

    global active_dinamic_menu
    msgUser = message  # берем msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)
    global phonenumber
    if message.contact is not None:
        if edit2['is'] == 0:
            active_dinamic_menu = 'kb_client_menu'
            msgBot = await bot.send_message(message.chat.id, 'Меню', reply_markup=arr['kb_client_menu'])
            msg_id_bot.append(msgBot)
            # print(msg_id)
        else:
            msgBot = await bot.send_message(message.chat.id, 'Меню', reply_markup=kb_client_menu2)
            msg_id_bot.append(msgBot)
            # print(msg_id)
        phonenumber= str(message.contact.phone_number)
        # для вывода в тг создаем список
        sp_phone[message.chat.id] = phonenumber


"""обработчики хендлеров главного меню"""
@dp.message_handler(lambda message: 'Где найти нужный тур?' in message.text)
async def maps(message : types.Message):
    msgUser = message  # берем msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)

    await bot.send_message(message.chat.id, paps, reply_markup=arr['kb_client_menu'])
    for i in msg_id_bot:  # удаляем все сообщения от бота
        await i.delete()
    msg_id_bot.clear()

    for i in msg_id_user:
        await i.delete()
    msg_id_user.clear()



# путеводитель по боту
paps = ('ГРОЗНЫЙ:\n----------\nМечеть Сердце Чечни\nГрозный Сити\nГрoзный Молл\nКофетун\nЧеченская государственная филармония\nНациональный музей Чеченской Республики\nНациональная библиотека Чеченской Республики\nИНДИВИДУАЛЬНЫЙ ТУР\n\n'
        'АРГУН:\n----------------\nМечеть имени Аймани Кадыровой "Сердце Матери"\nАргун-Сити\nФонтан\n\n'
        'ГУДЕРМЕС:\n-----------\nФонтан на проспекте Терешковой\nМемориал жертвам депортации\nВечный огонь памяти гудермесцев\n\n'
        'АКТИВ:\n------------\nРафтинг\nДайвинг\nКонные Прогулки\nПараплан\nВоздушный Шар\nВертолёт\nПарашют\n\n')


async def grozny(message: types.Message):
    global active_dinamic_menu
    active_dinamic_menu = 'grozny'
    msgUser = message  # берем msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)
    msgBot = await bot.send_message(message.chat.id, "Ваш выбор!", reply_markup=arr['grozny'])
    msg_id_bot.append(msgBot)

    # for i in msg_id: # удаляем сообщение от бота
    #     # print(i)
    #     await i.delete()
    # for i in msg_id_user: # удаляем сообщения от пользователя
    #     await i.delete()
    #     print(i)


async def argun(message: types.Message):
    global active_dinamic_menu
    active_dinamic_menu = 'argun'
    msgUser = message  # берем msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)

    msgBot = await bot.send_message(message.chat.id, "Ваш выбор!", reply_markup=arr['argun'])
    msg_id_bot.append(msgBot)

name_sud_vrem = []
# @dp.message_handler(commands="Вода")
async def gudermes(message : types.Message):

    global active_dinamic_menu
    active_dinamic_menu = 'gudermes'

    name_sud_vrem.append(1)
    msgUser = message  # берем msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)
    msgBot = await bot.send_message(message.chat.id, "Ваш выбор!", reply_markup=arr['gudermes'])
    msg_id_bot.append(msgBot)


# @dp.message_handler(commands="Воздух")
async def vozduh(message : types.Message):
    global active_dinamic_menu
    active_dinamic_menu = 'activ'
    msgUser = message  # берем msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)
    msgBot = await bot.send_message(message.chat.id, "Ваш выбор!", reply_markup=arr['activ'])
    msg_id_bot.append(msgBot)


async def add_button(message : types.Message):
    if str(message.from_user.id) in excel_files:
        global is_state_button
        is_state_button = [1]
        await bot.send_message(message.chat.id, "Введите название новой кнопки")


async def del_button(message : types.Message):
    if str(message.from_user.id) in excel_files:
        global is_state_button
        is_state_button = [2]

        arr = dinamic_kbs(admin_group(message.chat.id, admin_dict), 1)  # str(message['from']['id']) in excel_files

        await bot.send_message(message.chat.id, "Выберите кнопку из списка, которую необходимо удалить", reply_markup=arr[active_dinamic_menu])


async def db_photos(message : types.Message):
    arr = more_media(active_dinamic_menu)
    await bot.send_message(message.chat.id, "Выберите тур с которым хотите ознакомиться", reply_markup=arr[active_dinamic_menu])


'''************База данных для загрузки фото***************************'''
ID = None


# выгрузка из бд
async def more_categ_photos(message: types.Message):
    read = await sql_read3(name_table=message.text.split(" ")[1])  # возвращает фото, или False
    arr = more_media(active_dinamic_menu)
    if read:
        for i in read:
            time.sleep(0.5)
            await bot.send_photo(message.from_user.id, i[0], f'{i[1]}\nОписание: {i[2]}', reply_markup=arr[active_dinamic_menu])
    else:
        await bot.send_message(message.chat.id, "Фото пока нет", reply_markup=arr[active_dinamic_menu])


class FSMAdmin(StatesGroup):
    categ = State()
    images = State()
    name_categ_buttons = State()
    descriptions = State()


settings_phot = [0]
async def make_changes_command(message: types.Message):
    global ID, settings_phot
    ID = message.from_user.id
    settings_phot = [1]  # чтобы значок сменить при настройки фото, если тут 1 мы узнаем в каком менью добавить этот значок
    await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=button_case_admin2)
    await message.delete()


async def cm_start_photo(message: types.Message):
    global settings_phot
    if message.from_user.id == ID:
        settings_phot = [1]
        await FSMAdmin.categ.set()
        arr = more_media(active_dinamic_menu)
        await message.answer('Выберите категорию куда хотите загрузить фото!', reply_markup=arr[active_dinamic_menu])


# Ловим первый ответ и пишем в словарь
async def write_name_load_photo(message: types.Message):
    global categ
    if message.from_user.id == ID:
        categ = message.text.split(" ")[1]  # убираем значок
        await FSMAdmin.next()
        await message.answer('Загрузи фото', reply_markup=cancel_kb)


async def load_photo_write(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['images'] = message.photo[0].file_id
        await FSMAdmin.next()
        # next() Ожидание следующего ответа
        await message.reply("Теперь введи название", reply_markup=cancel_kb)


# @dp.message_handler(state=FSMAdmin.name)
async def load_name_write(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Введи описание")


async def load_descrip(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['desc'] = message.text
        await bot.send_message(message.chat.id, "Сохранено", reply_markup=button_case_admin2)

        await sql_add_command2(state, categ)

        await state.finish()


# УДАЛЕНИЯ

async def delete_categ_photo(message: types.Message):
    global settings_phot
    settings_phot = ['delcat']
    arr = more_media(active_dinamic_menu)
    await bot.send_message(message.chat.id, "Откуда хотите удалить фото?", reply_markup=arr[active_dinamic_menu])


async def sql_delete_command(data, del_photo):
    con = sq.connect('tur_categ.db')
    cur = con.cursor()
    con.execute(f'DELETE FROM {del_photo} WHERE name == ?', (data,))
    con.commit()


# хендлер для ответа и след для удаления
#2
# если событие 'del ' то запускается это функция
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('dell '))
async def del_callback_run_cat(callback_queryyy: types.CallbackQuery):
    global del_photo
    await sql_delete_command(callback_queryyy.data.replace('dell ', ''), del_photo=del_photo)
    await callback_queryyy.answer(text=f'{callback_queryyy.data.replace("dell ", "")} удалена.', show_alert=True)


async def delete_item_cat(message: types.Message):
    global del_photo
    del_photo = message.text.split(" ")[1]
    read = await sql_read3(name_table=message.text.split(" ")[1])
    if read:  # если фото есть удаляем
        for ret in read:
            print(len(ret[1].encode('utf-8')), '......................')
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}', reply_markup=AdminPanell)
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'dell {ret[1]}')))
    else:
        await bot.send_message(message.from_user.id, "У вас нет фото для удаления", reply_markup=button_case_admin2)

'''********************конец*****************************'''


async def save_new_buttons(message : types.Message):
    """Функции вызывет другу функцию (dinamic_kbs) для добавления кнопки, и отвечает пользователю что кнопка добавлена"""
    # print('save_new_buttons')

    global menu
    global is_state_button
    global active_dinamic_menu

    button_name = message['text']

    del_btn = 0

    if '[X]' in button_name:
        del_btn = button_name.split('[X] ')[1]

    if 1 in is_state_button:

        add_button_menu(button_name, active_dinamic_menu)

        arr = dinamic_kbs(admin_group(message.chat.id, admin_dict))  # str(message['from']['id']) in excel_files

        await bot.send_message(message.chat.id, "Кнопка успешно добавлена!", reply_markup=arr[active_dinamic_menu])

    elif 2 in is_state_button:

        del_button_new(del_btn, active_dinamic_menu)

        arr = dinamic_kbs(admin_group(message.chat.id, admin_dict))
        # arr = dinamic_kbs(str(message['from']['id']) in excel_files)

        await bot.send_message(message.chat.id, "Кнопка успешно удалена!", reply_markup=arr[active_dinamic_menu])

    is_state_button = [0]


async def all_handler(message : types.Message):

    # global active_dinamic_menu

    global is_state_button
    is_state_button = [0]

    # print(message)

    for option in menu:

        _name = option['name']

        for keyboard in option['keyboards']:

            _handler = keyboard['handler']

            if _handler != 'dat_ukaz' and _handler != 'none':

                for button in keyboard['buttons']:

                    text = button['text']
                    status = button['status']
                    if status == 1 and text == message.text:  # status 1 команда активна

                        # active_dinamic_menu = _name # сохраняем активное меню

                        await eval(_handler)(message)  # eval(_handler) перевод str в функцию и (message) запуск


cmnds = get_commands_client(menu) # определяет команду клиента используя словарь из client_commands.py, menu buttons in json

# фильтруем мат, и убираем маскируещие символы
# @dp.message_handler()
# async def echo_send(message : types.Message):
#     import json, string
#     print(message)
#     if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
#         .intersection(set(json.load(open('cenz.json')))) != set():
#         await message.reply('Маты запрещены')
#         await message.delete()


def regiter_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(contact, content_types=['contact'])
    dp.register_message_handler(otkr_menu, lambda message: message.text in ['Открыть меню ✅', 'Назад'] )
    dp.register_message_handler(file_excel_loader, lambda message: 'Вывести файл 📗' in message.text)
    dp.register_message_handler(add_button, lambda message: 'Добавить кнопку' in message.text)
    dp.register_message_handler(del_button, lambda message: 'Удалить кнопку' in message.text)
    dp.register_message_handler(db_photos, lambda message: 'Ознакомиться с турами 🏖' in message.text)

    dp.register_message_handler(make_changes_command, lambda message: 'Настройки фото 🛠' in message.text)
    dp.register_message_handler(cm_start_photo, lambda message: 'Добавить' in message.text, state=None)

    dp.register_message_handler(write_name_load_photo, state=FSMAdmin.categ)

    dp.register_message_handler(load_photo_write, content_types=['photo'], state=FSMAdmin.images)

    dp.register_message_handler(load_name_write, state=FSMAdmin.name_categ_buttons)

    dp.register_message_handler(load_descrip, state=FSMAdmin.descriptions)

    from handlers import correct_delete
    correct_delete.register_handlers_correct_delete(dp)  # перенесли сюда, чтобы не поймалсе его запрос функцией all_handler

    dp.register_message_handler(all_handler, lambda message: message.text in cmnds and cmnds != None)  # определяет нужную функцию используя словарь из kbs.py

    dp.register_message_handler(more_categ_photos, lambda message: message.text.startswith("🌄"))
    dp.register_message_handler(delete_categ_photo, lambda message: message.text.startswith("🗑"))
    dp.register_message_handler(delete_item_cat, lambda message: message.text.startswith("❌"))

    dp.register_message_handler(save_new_buttons, lambda message: message.text)
    # dp.register_message_handler(echo_send)


