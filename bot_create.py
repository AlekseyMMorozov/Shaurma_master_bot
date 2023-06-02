from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from bot_config import Shaurma_master_bot_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(Shaurma_master_bot_API)
dp = Dispatcher(bot, storage=storage)
