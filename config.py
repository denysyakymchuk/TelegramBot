from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '5258758589:AAGir_AD_CPWRSOEs4Jml7ORFOAbNiwwKA8'

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
