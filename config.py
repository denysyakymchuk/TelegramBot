import os

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import api_sheet

w_cancel = 'Отмена'
w_another = 'Другое'

n = {
   'actual_question': 0,
   'key_city': None
}

keyboards = api_sheet.main()
def get_keyboard(load=None):
   global keyboards
   if load is True:
      keyboards = api_sheet.main()
      return keyboards
   else:
      return keyboards


TOKEN = os.getenv('TOKEN')
bot = Bot(token='6538540132:AAG_qOJEahsERU9376p9HOwLjVGEWrBPlVs')

dp = Dispatcher(bot, storage=MemoryStorage())
