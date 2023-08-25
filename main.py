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
    o = OrderClass()
    match message.text:
        case 'all':
            d = o.get_orders()
            await message.answer(d)
        case 'one':
            d = o.one_order(1)
            await message.answer(d)
        case 'store':
            print(o.store_order('ivan', 128412, True, True))
        case 'update':
            print(o.update_order(id=1, reply_message="You are cool"))
        case 'delete':
            o.delete_order(1)
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
