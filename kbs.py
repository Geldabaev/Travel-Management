import json


def get_menu():

    "Берем кнопки из json"
    with open('json_kbs.json') as json_file:
        data = json.load(json_file)
    return data


def add_button_menu(button_name, menu_name):  # параметр функии название кнопки, и название меню
    "Добавляет кнопки"
    menu = get_menu()  # открываем кнопки которые у нас есть

    new_menu = []  # создаем список для новых кнопок

    for option in menu:

        _name = option['name']  # берем название кнопки, например Аргун

        if _name == menu_name:  # если Аргун и Активное(абхазия например) меню совпадают, другими словами смотрим куда нам в какое меню нам добавить кнопки

            new_keyboards = []

            for keyboard in option['keyboards']:  # перебираем все его под кнопки, напр: красная поляна
                _handler = keyboard['handler']  # берем хендлер дат указ

                new_keyboards.append(keyboard)  # дабавляем кнопки в новую клаву

            new_keyboards.append({  # добавляем инфо об этой кнопки
                'buttons': [
                    {
                        'text': button_name,
                        'status': 1
                    }
                ],
                'handler': _handler  # и хендлер дат указ
            })

            new_menu.append({  # добавляем всё это в новую клавиатуру
                'name': _name,  # добавляем под название абхазия(например) новые нопки
                'keyboards': new_keyboards  # новые кнопки
            })

        else:
            new_menu.append(option)  # то что не совпадает оставляем как есть, тс добавляем как есть при создания новой кнопки

    with open('json_kbs.json', 'w') as outfile:
        json.dump(new_menu, outfile)


def del_button_new(button_name, menu_name):
    menu = get_menu()

    new_menu = []

    for option in menu:

        _name = option['name']

        if _name == menu_name:

            new_keyboards = []

            for keyboard in option['keyboards']:

                _handler = keyboard['handler']

                new_buttons = []

                for button in keyboard['buttons']:

                    text = button['text']

                    if text != button_name:  # тоже самое что при создании, тольку теперь при создании новой клавы, мы пропускаем кнопку которую мы указали и-
                                            # таким образов удалем кнопку
                        new_buttons.append(button)

                new_keyboards.append({
                    'buttons': new_buttons,
                    'handler': _handler
                })

            new_menu.append({
                'name': _name,
                'keyboards': new_keyboards
            })

        else:
            new_menu.append(option)

    with open('json_kbs.json', 'w') as outfile:
        json.dump(new_menu, outfile)

    # print(data)


# menu = [
#     {
#         'name': 'kb_client_menu',
#         'keyboards': [
#             {
#                 'buttons': [
#                     {
#                         'text': 'Где найти нужный тур?',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 'maps'
#             },
#             {
#                 'buttons': [
#                     {
#                         'text': 'СOЧИ',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 'sochy'
#             },
#             {
#                 'buttons': [
#                     {
#                         'text': 'АБХАЗИЯ',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 'abhaz'
#             },
#             {
#                 'buttons': [
#                     {
#                         'text': 'МОРЕ',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 'voda'
#             },
#             {
#                 'buttons': [
#                     {
#                         'text': 'АКТИВ',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 'vozduh'
#             },
#             {
#                 'buttons': [
#                     {
#                         'text': 'Индивид',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 'none'
#             },
#             {
#                 'buttons': [
#                     {
#                         'text': 'ДРУГОЕ',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 0
#             },
#             {
#                 'buttons': [
#                     {
#                         'text': 'Корректировка заявки',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 'none'
#             },
#             {
#                 'buttons': [
#                     {
#                         'text': 'Отмена заявки',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 'none'
#             },
#         ],
#         'type': 'row'
#     },
#     # sochi
#     {
#         'name': 'sochi',
#         'keyboards': [
#             {
#                 'buttons': [
#                     {
#                         'text': 'Красная Поляна',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Обзорная Сочи',
#                         'status': 1
#                     },
#                     {
#                         'text': '33 Водопада',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Воронцовские пещеры',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Каньоны Псахо (джип-тур)',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Мамонтово Ущелье (джип-тур)',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Эпоха времени',
#                         'status': 1
#                     },
#                 ],
#                 'handler': 'dat_ukaz'
#             }
#         ],
#         'type': 'row'
#     },
#     # abkhazia
#     {
#         'name': 'abkhazia',
#         'keyboards': [
#             {
#                 'buttons': [
#                     {
#                         'text': 'Золотое Кольцо',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Абхазское застолье',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Термальные Источники',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Абхазский драйв (джип-тур)',
#                         'status': 1
#                     },
#                 ],
#                 'handler': 'dat_ukaz'
#             }
#         ],
#         'type': 'row'
#     },
#     # more
#     {
#         'name': 'more',
#         'keyboards': [
#             {
#                 'buttons': [
#                     {
#                         'text': 'Морская прогулка',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Рыбалка в море',
#                         'status': 1
#                     },
#                     {
#                         'text': 'АРЕНДА ЯХТ',
#                         'status': 1
#                     }
#                 ],
#                 'handler': 'dat_ukaz'
#             }
#         ],
#         'type': 'row'
#     },
#     # activ
#     {
#         'name': 'activ',
#         'keyboards': [
#             {
#                 'buttons': [
#                     {
#                         'text': 'Рафтинг',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Квадроциклы',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Конные Прогулки',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Солохаул (джип-тур)',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Дайвинг',
#                         'status': 1
#                     },
#                     {
#                         'text': 'Параплан',
#                         'status': 1
#                     },
#                 ],
#                 'handler': 'dat_ukaz'
#             }
#         ],
#         'type': 'row'
#     }
# ]
#
# with open('json_kbs.json', 'w') as outfile:
#     json.dump(menu, outfile)