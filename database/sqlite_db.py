import sqlite3 as sq
from datetime import datetime
from bot_create import bot


def sql_start():
    global base, curs
    base = sq.connect('shaurma_db.db')
    curs = base.cursor()
    if base:
        print(f'{datetime.now()} - База данных {base} успешно подключена')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


async def add_menu_db(state):
    async with state.proxy() as data:
        curs.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()
        print(f'{datetime.now()} - в базу данных добавлено значение {tuple(data.values())}')


async def get_menu_from_db(message):
    for ex in curs.execute('SELECT * FROM menu').fetchall():
        print(f'{datetime.now()} - {ex[0]} {ex[1]} {ex[2]} {ex[3]}')
        await bot.send_photo(message.from_user.id, ex[0], f'{ex[1]},\nОписание: {ex[2]}.\nСтоимость: {ex[3]} руб.')


async def del_menu_db(data):
    curs.execute('DELETE FROM menu WHERE name == ?', (data,))
    print(f'{datetime.now()} - объеект {data} удален из БД')
    base.commit()


async def sql_read():
    pos = curs.execute('SELECT * FROM menu').fetchall()
    print(f'{datetime.now()} - чтение {pos} из БД')
    return pos


