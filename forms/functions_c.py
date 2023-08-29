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
    mess = int(message.text)
    print(type(mess))
    if isinstance(mess, int):
        n['total'] = '{:,}'.format(mess).replace(',', ' ')
        await state.finish()
        n['actual_question'] = 2
        n['id_th'] = message.chat.id
        await Functions().send_city_to(message.chat.id)
    else:
        await message.reply("Только цифры!")
        await StateTotal.get_total.set()



class Functions:
    def __init__(self):
        self.buttons = get_keyboard()

    async def send_city_from(self, message):
        keyboard = send_paginated_buttons(page=1, number_cell=0, button_list_domestic=self.buttons)
        await bot.send_message(message, "Выберите из какого города хотите переслать:", reply_markup=keyboard)

    async def send_currency(self, message, selected_city):
        cities = serializator.search_city(self.buttons, selected_city)
        n['key_city'] = cities
        keyboard = send_paginated_buttons(page=1, number_cell=1, button_list_domestic=self.buttons, is_city=cities)
        await bot.send_message(message, "Выберите в какой валюте:", reply_markup=keyboard)

    async def send_total(self, message):
        n['key_city'] = None
        await bot.send_message(message, "Введите сумму:")
        await StateTotal.get_total.set()

    async def send_city_to(self, message):
        keyboard = send_paginated_buttons(page=1, number_cell=2, button_list_domestic=self.buttons)
        await bot.send_message(message, "Выберите в какой город:", reply_markup=keyboard)

    async def send_currency_to(self, message, selected_city):
        cities = serializator.search_city(self.buttons, selected_city)
        n['key_city'] = cities
        keyboard = send_paginated_buttons(page=1, number_cell=3, button_list_domestic=self.buttons, is_city=cities)
        await bot.send_message(message, "Выберите в какой валюте получить:", reply_markup=keyboard)

    async def send_currency_view(self, message):
        n['key_city'] = None
        keyboard = send_paginated_buttons(page=1, number_cell=4, button_list_domestic=self.buttons)
        await bot.send_message(message, "Выберите в каком виде получить:", reply_markup=keyboard)