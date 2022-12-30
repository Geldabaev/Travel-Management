from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiogram.utils.markdown as fmt

# открыть меню
kb_button_individual = KeyboardButton('Индивид.')  # будут приниматься как тур, и после них сразу дата
kb_button_other = KeyboardButton('ДРУГОЕ')  # будут приниматься как тур, и после них сразу дата


# Оставляем
# открыть меню
zz = KeyboardButton('Открыть меню ✅')
oz = KeyboardButton("Галерея 🖼")
UrlGener = KeyboardButton("Получить реферальную ссылку 💵")
zz_zayav = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
zz_zayav.add(zz).add(oz).add(UrlGener)

# Оставляем
# поделиться контактом
b1 = KeyboardButton('Поделиться', request_contact=True)
kb_contact = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #resize_keyboard=True уменьшаем кнопки, one_time_keyboard=True одноразовая клавиатура
kb_contact.row(b1)

# сегодня зватра
kb_today = KeyboardButton('Сегодня')
kb_tomorrow = KeyboardButton('Завтра')
cancel = KeyboardButton('Отмена')
kb_today_tomorrow = ReplyKeyboardMarkup(resize_keyboard=True)
kb_today_tomorrow.row(kb_today, kb_tomorrow).row(cancel)


# сколько взрослых
sko_vz_button1 = KeyboardButton('1')
sko_vz_button2 = KeyboardButton('2')
sko_vz_button3 = KeyboardButton('3')
sko_vz_button4 = KeyboardButton('4')
sko_vz_button5 = KeyboardButton('5')

sko_vz_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
sko_vz_markup.row(sko_vz_button1, sko_vz_button2, sko_vz_button3, sko_vz_button4, sko_vz_button5).row(cancel)


# Сколько детей с посадочным местом
pos_bes_button1 = KeyboardButton('1')
pos_bes_button2 = KeyboardButton('2')
pos_bes_button3 = KeyboardButton('3')
pos_bes_button4 = KeyboardButton('4')
pos_bes_button5 = KeyboardButton('5')
pos_bes_button0 = KeyboardButton('0')

pos_bes_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
pos_bes_markup.row(pos_bes_button0, pos_bes_button1, pos_bes_button2, pos_bes_button3, pos_bes_button4, pos_bes_button5).row(cancel)


# окно помощи
kb_tel = InlineKeyboardMarkup(row_width=1)
kb_t = InlineKeyboardButton(text='Если несколько, введите через пробел', callback_data='номер')
kb_tel.add(kb_t)


dop_in = InlineKeyboardMarkup(row_width=1)
kb_dop_in = InlineKeyboardButton(text='Время выезда, если есть выбор', callback_data='информация')
dop_in.add(kb_dop_in)


#подверждение
kb_ver = KeyboardButton('ВСЁ ВЕРНО')
kb_isp = KeyboardButton('ИСПРАВИТЬ')
kb_ver_isp = ReplyKeyboardMarkup(resize_keyboard=True)
kb_ver_isp.row(kb_ver, kb_isp).row(cancel)


# Да Нет
yes = KeyboardButton('Да')
now = KeyboardButton('Нет')
yes_now = ReplyKeyboardMarkup(resize_keyboard=True)
yes_now.row(yes, now).row(cancel)


# корректировать
kb_nazat = KeyboardButton('Отмена')
nazat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
nazat_markup.add(kb_nazat)


# новое главное меню при корректировке
# открыть меню
kb_menu11 = KeyboardButton('ГРОЗНЫЙ')
kb_menu21 = KeyboardButton('АРГУН')
kb_menu31 = KeyboardButton('ГУДЕРМЕС')
kb_menu41 = KeyboardButton('АКТИВ')
kb_client_menu2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_menu2.row(kb_menu11, kb_menu21).row(kb_menu31, kb_menu41).row(kb_button_individual, kb_button_other)


net = KeyboardButton('Нет')
net_markup = ReplyKeyboardMarkup(resize_keyboard=True)
net_markup.add(net)


# Отмена клавиатура
exit = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
exit.add(cancel)
