from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b_add = KeyboardButton('/add')
b_del = KeyboardButton('/del')
b_help = KeyboardButton('/list')


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.row(b_add, b_del).add(b_help)

