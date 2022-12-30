import sqlite3 as sq
from sqlite3 import OperationalError

__all__ = ['sql_add_command2', 'sql_start_categ', 'sql_read3']


# загрузка фото в бд
async def sql_add_command2(state, name_db):
    with sq.connect(f'tur_categ.db') as con:
        cur = con.cursor()

        cur.execute(f'CREATE TABLE IF NOT EXISTS {name_db}(img TEXT, name TEXT, description TEXT)')
    async with state.proxy() as data:
        cur.execute(f'INSERT INTO {name_db} VALUES(?, ?, ?)', tuple(data.values()))
        # tuple переводит в кортеж
        con.commit()


def sql_start_categ():
    "соединение с базой данных"
    global con, cur
    con = sq.connect('tur_categ.db')
    cur = con.cursor()
    if con:
        print('Data base categ connected OK!')
    cur.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT)')
    con.commit()


async def sql_read3(name_table):
    # соединение с нужной таблицей
    sql_start_categ()
    try:
        all_photos = con.execute(f'SELECT * FROM {name_table}').fetchall()
        # print(all_photos)
        if all_photos:
            return all_photos
        return False  # если база данных есть но фото нет
    except OperationalError as ex:
        print(ex)
        return False  # если совсем нет таблица в бд