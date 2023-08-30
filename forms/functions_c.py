from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import get_keyboard
import serializator
from config import bot, dp, n
from keyboard.inline_form import send_paginated_buttons


class StateTotal(StatesGroup):
    get_total = State()


@dp.message_handler(state=StateTotal.get_total)
async def get_total(message: types.Message, state: FSMContext):
    try:
        try:
            mess = int(message.text)
        except:
            await message.reply("Must be only numbers!")
            await StateTotal.get_total.set()

        if isinstance(mess, int):
            n['total'] = '{:,}'.format(mess).replace(',', ' ')
            n['actual_question'] = 2
            n['id_th'] = message.chat.id
            await state.finish()
            await Functions().send_city_to(message.chat.id)
        else:
            await message.reply("Must be only numbers!")
            await StateTotal.get_total.set()

    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")


class Functions:
    def __init__(self):
        self.buttons = get_keyboard()

    async def send_city_from(self, message):
        try:
            keyboard = send_paginated_buttons(page=1, number_cell=0, button_list_domestic=self.buttons)
            await bot.send_message(message, "Select from which city you want to send.", reply_markup=keyboard)

        except Exception as error:
            from logconfig import setup_logging
            logger = setup_logging()
            logger.error(f"{error}")

    async def send_currency(self, message, selected_city):
        try:
            cities = serializator.search_city(self.buttons, selected_city)
            n['key_city'] = cities
            keyboard = send_paginated_buttons(page=1, number_cell=1, button_list_domestic=self.buttons, is_city=cities)
            await bot.send_message(message, "Select in which currency:", reply_markup=keyboard)

        except Exception as error:
            from logconfig import setup_logging
            logger = setup_logging()
            logger.error(f"{error}")

    async def send_total(self, message):
        try:
            n['key_city'] = None
            await bot.send_message(message, "Enter the amount:")
            await StateTotal.get_total.set()

        except Exception as error:
            from logconfig import setup_logging
            logger = setup_logging()
            logger.error(f"{error}")

    async def send_city_to(self, message):
        try:
            keyboard = send_paginated_buttons(page=1, number_cell=2, button_list_domestic=self.buttons)
            await bot.send_message(message, "Select the city to send to:", reply_markup=keyboard)

        except Exception as error:
            from logconfig import setup_logging
            logger = setup_logging()
            logger.error(f"{error}")

    async def send_currency_to(self, message, selected_city):
        try:
            cities = serializator.search_city(self.buttons, selected_city)
            n['key_city'] = cities
            keyboard = send_paginated_buttons(page=1, number_cell=3, button_list_domestic=self.buttons, is_city=cities)
            await bot.send_message(message, "Select the currency to receive in:", reply_markup=keyboard)

        except Exception as error:
            from logconfig import setup_logging
            logger = setup_logging()
            logger.error(f"{error}")
