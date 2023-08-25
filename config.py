import os

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

w_cancel = 'Отмена'
w_another = 'Другое'
w_another_ag = 'Еще другое'

TOKEN = os.getenv('TOKEN')

bot = Bot(token='6538540132:AAG_qOJEahsERU9376p9HOwLjVGEWrBPlVs')

dp = Dispatcher(bot, storage=MemoryStorage())
