from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

open_menu = KeyboardButton('Открыть меню ✅')
oz = KeyboardButton("Галерея 🖼")
UrlGener = KeyboardButton("Получить реферальную ссылку 💵")
resbutton = KeyboardButton("Сброс изменения кнопок 💥")
open_file = KeyboardButton('Вывести файл 📗')
AdminPanell = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
AdminPanell.add(open_menu).add(oz).add(UrlGener).row(resbutton, open_file)


button_load = KeyboardButton('Загрузить')
button_delete = KeyboardButton('Удалить')
cancel_button = KeyboardButton('Выход')
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_delete).add(cancel_button)



button_load = KeyboardButton('Добавить')
cancel_button = KeyboardButton('Назад')
button_case_admin2 = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load).add(cancel_button)

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(cancel_button)
