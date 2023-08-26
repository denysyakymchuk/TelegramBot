from aiogram import executor, types
from aiogram.types import callback_query

from database.crud.order import OrderClass
from database.crud.operator import OperatorClass
from keyboard.inline_buttons import button_spam
from keyboard.keyboard import default_cities
from state import register_handlers, StateOrder
from config import dp, bot

register_handlers(dp)


@dp.message_handler(commands=['start'],  state=None)
async def send_welcome(message: types.Message):
    await message.reply("Привет! Город откуда хотите переслать:", reply_markup=default_cities)
    await StateOrder.city_from.set()

#-------------------------------------------------------------------------


@dp.callback_query_handler()
async def on_inline_button(callback_query: types.CallbackQuery):
    cart = callback_query.data.split(':')

    if cart[0] == 'accept_id':
        pass
        await callback_query.message.reply(f"Вы приняли заказ: Имя: {cart[1]}, id:{cart[2]}\nОн будет проинформирован")
    elif cart[0] == 'cancel_id':
        pass
        await callback_query.message.reply(f"Вы отказали: Имя: {cart[1]}, id:{cart[2]}\nОн будет проинформирован")
    else:
        return KeyError
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


#-------------------------------------------------------------------------#-------------------------------------------------------------------------



@dp.message_handler()
async def echo(message: types.Message):
    o = OrderClass()
    op = OperatorClass()
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
        case 'new admin':
            op.store_operator(message.chat.first_name, message.chat.id)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
