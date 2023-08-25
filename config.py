from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

w_cancel = 'Отмена'
w_another = 'Другое'
w_another_ag = 'Еще другое'

API_TOKEN = '6538540132:AAG_qOJEahsERU9376p9HOwLjVGEWrBPlVs'

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
