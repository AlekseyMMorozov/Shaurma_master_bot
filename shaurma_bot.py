from aiogram.utils import executor
from datetime import datetime
from bot_create import dp
from bot_handlers import client, admin, common
from database import sqlite_db

async def on_startup(_):
    print(f'{datetime.now()} - Мастер шаурмы онлайн')
    sqlite_db.sql_start()


client.register_handler_client(dp)
admin.register_handler_admin(dp)
common.register_handler_common(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
