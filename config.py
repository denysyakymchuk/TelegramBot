import os

import loguru
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import api_sheet

n = {
   'actual_question': 0,
   'key_city': None
}
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

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
