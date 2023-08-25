import logging


from aiogram import Bot, Dispatcher, executor, types

import state
from keyboard import default_cities
from state import register_handlers, StateOrder
from config import dp

register_handlers(dp)


@dp.message_handler(commands=['start'],  state=None)
async def send_welcome(message: types.Message):
    await message.reply("Привет! Напишите сейчас c какого города хотите переслать:", reply_markup=default_cities)
    await StateOrder.city_from.set()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
