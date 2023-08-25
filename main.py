from aiogram import Bot, Dispatcher, executor, types

from database.crud.operator import OperatorClass
from database.crud.order import OrderClass
from keyboard import default_cities
from state import register_handlers, StateOrder
from config import dp

register_handlers(dp)


@dp.message_handler(commands=['start'],  state=None)
async def send_welcome(message: types.Message):
    await message.reply("Привет! Город откуда хотите переслать:", reply_markup=default_cities)
    await StateOrder.city_from.set()


@dp.message_handler()
async def echo(message: types.Message):
    o = OperatorClass()
    match message.text:
        case 'all':
            d = o.get_operators()
            await message.answer(d)
        case 'one':
            d = o.one_operator(1)
            await message.answer(d)
        case 'store':
            print(o.store_operator('ivan', 128412))
        case 'update':
            print(o.update_operator(1,'VASYYL', 2423))
        case 'delete':
            o.delete_operators(1)
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
