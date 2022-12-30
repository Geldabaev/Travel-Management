import random
import sqlite3 as sq
from excel_loader import phone_number


def generate_url(username):
    "Генерация реферальной ссылки"
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    for i in range(7):
        password += random.choice(chars)
    password = f'https://t.me/{username}?start={password}'  #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    print(password)
    return password


def generate_code():
    "Генерация реферальной ссылки"
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    for i in range(7):
        password += random.choice(chars)

    print(password)
    return password


def create_db():
    """Создает таблицы бызы данных"""
    with sq.connect("refer.db") as con:
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS referals(
                       user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       code TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS user_info(
                       user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_name TEXT,
                       url_user TEXT,
                       url_bot TEXT)""")


def db_true_false(msgid):
    """проверяет есть ли у пользователя реф ссылка, если нет, дает возможность создать новый, и сохраняет его"""
    con = sq.connect("refer.db")
    print("connect refer.db")
    cur = con.cursor()

    # cur.execute(f"SELECT name FROM ishak WHERE name = :msgid", {"msgid": msgid})
    cur.execute("SELECT user_id FROM referals WHERE user_id LIKE ?", (msgid,))

    try:
        return cur.fetchall()[0][0]
    except IndexError as ex:
        print(ex)
        return False
    finally:
        con.close()


def WriteReferDB(id, user_code, user_name, user_url, user_name_bot):
    # запись в базе реф ссылку на айди пользователя
    # создаем уникальный код
    with sq.connect("refer.db") as con:
        cur = con.cursor()

        cur.execute("INSERT INTO referals VALUES(?, ?)", (id, user_code))
        print(f"{id}, {user_name,} {user_url}, {user_name_bot}")
        cur.execute("INSERT INTO user_info VALUES(?, ?, ?, ?)", (int(id), user_name, user_url, user_name_bot))
        return True


def mailref(msg):
    "отправка из бд его реф ссылку"
    with sq.connect("refer.db") as con:
        cur = con.cursor()

        cur.execute("SELECT code FROM referals WHERE user_id LIKE ?", (msg.chat.id,))

        return cur.fetchall()[0][0]


def mail_info_refer(code):
    """Берет данные владельцы ссылки для отправки админу"""
    with sq.connect('refer.db') as con:
        cur = con.cursor()

        cur.execute("""SELECT user_info.user_id, user_name, url_user, referals.code, user_info.url_bot
                       FROM user_info
                       JOIN referals ON referals.user_id = user_info.user_id
                       WHERE referals.code = ?""", (code,))

        return cur.fetchall()
