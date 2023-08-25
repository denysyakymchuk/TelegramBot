from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

w_cancel = 'Отмена'
w_another = 'Другое'
w_another_ag = 'Еще другое'

API_TOKEN = '5258758589:AAGir_AD_CPWRSOEs4Jml7ORFOAbNiwwKA8'

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
