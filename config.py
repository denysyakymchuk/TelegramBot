import os

import loguru
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import api_sheet

w_cancel = 'Отмена'
w_another = 'Другое'

n = {
   'actual_question': 0,
   'key_city': None
}
api_id = '26785918'
api_hash = 'd53e51145a15e59436e81f52639906fe'
phone_number = '+48507635321'
keyboards = api_sheet.main()


def get_keyboard(load=None):
   try:
      global keyboards
      if load is True:
         keyboards = api_sheet.main()
         return keyboards
      else:
         return keyboards

   except Exception as error:
      loguru.logger.critical(error)


TOKEN = os.getenv('TOKEN')
bot = Bot(token='6538540132:AAG_qOJEahsERU9376p9HOwLjVGEWrBPlVs')

dp = Dispatcher(bot, storage=MemoryStorage())
