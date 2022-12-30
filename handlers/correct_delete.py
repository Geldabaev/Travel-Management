from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from excel_loader import write_zayav
from keyboards import zz_zayav
from keyboards import yes_now, nazat_markup
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from handlers.client import otkr_menu, msg_id_user, msg_id_bot
from handlers.opros import edit
from excel_loader import edit2, delete_z
import json, string



number_correct = {}


# сработает на Корректировка заявки
class FSMAdvd(StatesGroup):
    # окна ввода данных
    # начинает название функции
    correc_isp_state = State()
    # продолжается через хендлеры
    number_zayav_state = State()
    yes_now_state = State()


# корректировка заявки
# начало fsm
# @dp.message_handler(lambda message: 'Корректировка заявки' in message.text)
async def correc_isp_state(message : types.Message):
    await FSMAdvd.number_zayav_state.set()
    print(message)
    # отвечаем и удаляем клавиатуру если есть
    await bot.send_message(message.chat.id, "Введите номер вашей заявки", reply_markup=ReplyKeyboardRemove())



# Выход из состояний где бы не находились
@dp.message_handler(state="*", commands='Отмена')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    msgUser = message  # берем msg пользователя, чтобы потом удалить его
    msg_id_user.append(msgUser)
    print(message)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.chat.id, 'Главное меню', reply_markup=zz_zayav)
    for i in msg_id_user:
        await i.delete()
    for i in msg_id_bot:
        await i.delete()
    msg_id_user.clear()
    msg_id_bot.clear()

# ловим первый ответ
@dp.message_handler(state=FSMAdvd.number_zayav_state)
async def numb_zay(message : types.Message, state: FSMContext):
    global number, number_correct
    print(message)
    number_correct['cor'] = message.text
    number = message.text
    # если заявка найдена спрашиваем эта ваша заявка
    try:
        try:
            user_name, sp_phone, sp_tur, data_day, vz_sk, stoim_vz, posadoch, stoim_chi_1, besplat, naz_bes, nom_tel_tur, dop_inf = write_zayav(number, message.chat.id)
            await bot.send_message(message.chat.id, f"Эту заявку корректируем?\n"
                                                    f"Клиент: {user_name} {sp_phone}\n"
                                                    f"Тур: {sp_tur}\n"
                                                    f"Дата: {data_day}\n"
                                                    f"Взрослые: {vz_sk} x {stoim_vz}\n"
                                                    f"Дети (платно): {posadoch} x {stoim_chi_1}\n"
                                                    f"Дети (бесплатно): {besplat}\n"
                                                    f"Остановка: {naz_bes}\n"
                                                    f"Телефон туриста: {nom_tel_tur}\n"
                                                    f"Доп. информация: {dop_inf}", reply_markup=yes_now)
            await FSMAdvd.next()  # режим ожидания
        except:
            # зпускаем хендлер как функцию отбрасывая назад пользователя
            otver = write_zayav(number, message.chat.id)
            await bot.send_message(message.chat.id, otver, reply_markup=zz_zayav)
    except:
        await bot.send_message(message.chat.id, "Такой заявки нет!")
        await bot.send_message(message.chat.id, "Введите номер вашей заявки", reply_markup=nazat_markup)



# ловим второй ответ да или нет
@dp.message_handler(state=FSMAdvd.yes_now_state)
async def yes_or_now(message : types.Message, state: FSMContext):
    global number
    print(message)
    if message.text == "Да":
        edit2['is'] = number
        edit['is'] = number

        await bot.send_message(message.chat.id, "Заполните данные, мы перезапишем вашу заявку")
        await state.finish()  # выходим из состояний
        await otkr_menu(message)
    else:
        await bot.send_message(message.chat.id, "Повторите")
        # вызывем хендлер как обычную функцию, отбрасывая его назад
        await correc_isp_state(message)


# отмена заявки ____________________
# сработает на отмена заявки
class FSMAotm(StatesGroup):
    # окна ввода данных
    # начинает название функции
    otmena = State()
    # продолжается через хендлеры
    number_otm_zayav_state = State()
    yes_now_otm_state = State()


# отмена заявки
# начало fsm
@dp.message_handler(lambda message: 'Отмена заявки' in message.text)
async def otmena(message : types.Message):
    await FSMAotm.number_otm_zayav_state.set()
    print(message)
    # отвечаем и удаляем клавиатуру если есть
    await bot.send_message(message.chat.id, "Введите номер вашей заявки", reply_markup=ReplyKeyboardRemove())


# ловим первый ответ
@dp.message_handler(state=FSMAotm.number_otm_zayav_state)
async def numb_zay_otm(message : types.Message, state: FSMContext):
    global number_otm, user_name, sp_phone
    print(message)
    number_otm = message.text
    # если заявка найдена спрашиваем эта ваша заявка
    try:
        try:
            user_name, sp_phone, sp_tur, data_day, vz_sk, stoim_vz, posadoch, stoim_chi_1, besplat, naz_bes, nom_tel_tur, dop_inf = write_zayav(number_otm, message.chat.id)
            await bot.send_message(message.chat.id, f"Эту заявку хотите отменить?\n"
                                                    f"Клиент: {user_name} {sp_phone}\n"
                                                    f"Тур: {sp_tur}\n"
                                                    f"Дата: {data_day}\n"
                                                    f"Взрослые: {vz_sk} x {stoim_vz}\n"
                                                    f"Дети (платно): {posadoch} x {stoim_chi_1}\n"
                                                    f"Дети (бесплатно): {besplat}\n"
                                                    f"Остановка: {naz_bes}\n"
                                                    f"Телефон туриста: {nom_tel_tur}\n"
                                                    f"Доп. информация: {dop_inf}", reply_markup=yes_now)
            await FSMAotm.next()  # режим ожидания
        except:
            # зпускаем хендлер как функцию отбрасывая назад пользователя
            otver = write_zayav(number_otm, message.chat.id)
            await bot.send_message(message.chat.id, otver, reply_markup=zz_zayav)
    except:
        await bot.send_message(message.chat.id, "Такой заявки нет!")
        await bot.send_message(message.chat.id, "Введите номер вашей заявки", reply_markup=nazat_markup)


# ловим второй ответ да или нет
@dp.message_handler(state=FSMAotm.yes_now_otm_state)
async def yes_now_otm(message : types.Message, state: FSMContext):
    global number_otm
    print(message)
    if message.text == "Да":
        otv = delete_z(message.chat.id, number_otm)
        # пресылаем в групп
        group_id = '-1001854126142'  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        next_id = number_otm
        await bot.send_message(group_id, f"Клиент: {user_name} {sp_phone}\n"
                                         f"Заявка под номером {next_id} отменена!")

        await bot.send_message(message.chat.id, otv, reply_markup=zz_zayav)
        await state.finish()  # выходим из состояний

    else:
        await bot.send_message(message.chat.id, "Повторите")
        # вызывем хендлер как обычную функцию, отбрасывая его назад
        await otmena(message)


# Регистрируем хендлеры
def register_handlers_correct_delete(dp : Dispatcher):
    # машинное состояние
    dp.register_message_handler(correc_isp_state, lambda message: message.text in 'Корректировка заявки' or message.text in 'Нет', state=None)
