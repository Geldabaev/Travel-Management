from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    print("Бот вышел в онлайн")
    # передать в executor


# запускаем зарегистрированные хендлеры
from handlers import client, opros, correct_delete
from data_base import sqlite_db
# from washed_del import washed


sqlite_db.register_handlers_admin(dp)
opros.register_handlers_opros(dp)
client.regiter_handlers_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
