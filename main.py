import logging


from aiogram import Bot, Dispatcher, executor, types

import state
from state import register_handlers, StateOrder
from config import dp

register_handlers(dp)


@dp.message_handler(commands=['start'],  state=None)
async def send_welcome(message: types.Message):
    await message.reply("Привет! Напишите сейчас с какого города хотите переслать:")
    await StateOrder.city_from.set()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
