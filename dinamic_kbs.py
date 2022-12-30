from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiogram.utils.markdown as fmt
from kbs import get_menu
from aiogram import types
import json
from create_bot import dp, bot


def dinamic_kbs(is_admin, is_del_mode = 0):

    menu = get_menu()

    arr = {}

    for option in menu:

        _name = option['name']

        arr[_name] = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        for keyboard in option['keyboards']:

            # _handler = keyboard['handler']

            for button in keyboard['buttons']:

                text = button['text']

                if is_del_mode:
                    text = "[X] " + text

                status = button['status']

                button = KeyboardButton(text)
                arr[_name].row(button)

        if is_admin and is_del_mode == 0:
            add_btn = KeyboardButton('⚙ Добавить кнопку')
            del_btn = KeyboardButton('⛔ Удалить кнопку')
            button_delete = KeyboardButton('🗑 Удалить фото')
            photo_gall = KeyboardButton('Ознакомиться с турами 🏖')
            add_photo = KeyboardButton('Настройки фото 🛠')
            arr[_name].row(photo_gall).row(add_photo).add(add_btn).row(button_delete, del_btn)
        elif is_del_mode == 0:  # если он не админ
            photo_gall = KeyboardButton('Ознакомиться с турами 🏖')
            arr[_name].row(photo_gall)
        else:  # просто на всякий
            photo_gall = KeyboardButton('Ознакомиться с турами 🏖')
            arr[_name].row(photo_gall)

    return arr


@dp.message_handler(lambda message: "Сброс изменения кнопок 💥" in message.text)
async def ResetButtons(message : types.Message):
    "Создает json с конпками, или сброс изменений"
    menu = [
        {
            'name': 'kb_client_menu',
            'keyboards': [
                {
                    'buttons': [
                        {
                            'text': 'Где найти нужный тур?',
                            'status': 1
                        }
                    ],
                    'handler': 'maps'
                },
                {
                    'buttons': [
                        {
                            'text': 'ГРОЗНЫЙ',
                            'status': 1
                        }
                    ],
                    'handler': 'grozny'  # func
                },
                {
                    'buttons': [
                        {
                            'text': 'АРГУН',
                            'status': 1
                        }
                    ],
                    'handler': 'argun'
                },
                {
                    'buttons': [
                        {
                            'text': 'ГУДЕРМЕС',
                            'status': 1
                        }
                    ],
                    'handler': 'gudermes'
                },
                {
                    'buttons': [
                        {
                            'text': 'АКТИВ',
                            'status': 1
                        }
                    ],
                    'handler': 'vozduh'
                },
                {
                    'buttons': [
                        {
                            'text': 'ДРУГОЕ',
                            'status': 1
                        }
                    ],
                    'handler': 0
                },
                {
                    'buttons': [
                        {
                            'text': 'Индивид.',
                            'status': 1
                        }
                    ],
                    'handler': 0
                },
                {
                    'buttons': [
                        {
                            'text': 'Корректировка заявки',
                            'status': 1
                        }
                    ],
                    'handler': 'none'
                },
                {
                    'buttons': [
                        {
                            'text': 'Отмена заявки',
                            'status': 1
                        }
                    ],
                    'handler': 'none'
                },
            ],
            'type': 'row'
        },
        # grozny
        {
            'name': 'grozny',
            'keyboards': [
                {
                    'buttons': [
                        {
                            'text': 'Мечеть Сердце Чечни',
                            'status': 1
                        },
                        {
                            'text': 'Грозный Сити',
                            'status': 1
                        },
                        {
                            'text': 'Грoзный Молл',  # анг o, чтобы небыло конфликтов
                            'status': 1
                        },
                        {
                            'text': 'Чеченская государственная филармония',
                            'status': 1
                        },
                        {
                            'text': 'Национальный музей Чеченской Республики',
                            'status': 1
                        },
                        {
                            'text': 'Национальная библиотека Чеченской Республики',
                            'status': 1
                        },
                        {
                            'text': 'Кофетун',
                            'status': 1
                        },
                    ],
                    'handler': 'dat_ukaz'
                }
            ],
            'type': 'row'
        },
        # argun
        {
            'name': 'argun',
            'keyboards': [
                {
                    'buttons': [
                        {
                            'text': 'Мечеть имени Аймани Кадыровой "Сердце Матери"',
                            'status': 1
                        },
                        {
                            'text': 'Аргун-Сити',
                            'status': 1
                        },
                        {
                            'text': 'Фонтан',
                            'status': 1
                        },
                    ],
                    'handler': 'dat_ukaz'
                }
            ],
            'type': 'row'
        },
        # gudermes
        {
            'name': 'gudermes',
            'keyboards': [
                {
                    'buttons': [
                        {
                            'text': 'Фонтан на проспекте Терешковой',
                            'status': 1
                        },
                        {
                            'text': 'Мемориал жертвам депортации',
                            'status': 1
                        },
                        {
                            'text': 'Вечный огонь памяти гудермесцев',
                            'status': 1
                        }
                    ],
                    'handler': 'dat_ukaz'
                }
            ],
            'type': 'row'
        },
        # activ
        {
            'name': 'activ',
            'keyboards': [
                {
                    'buttons': [
                        {
                            'text': 'Рафтинг',
                            'status': 1
                        },
                        {
                            'text': 'Конные Прогулки',
                            'status': 1
                        },
                        {
                            'text': 'Дайвинг',
                            'status': 1
                        },
                        {
                            'text': 'Параплан',
                            'status': 1
                        },
                    ],
                    'handler': 'dat_ukaz'
                }
            ],
            'type': 'row'
        }
    ]

    with open('json_kbs.json', 'w') as outfile:
        json.dump(menu, outfile)

    await bot.send_message(message.chat.id, "Кнопки востановлены!")
