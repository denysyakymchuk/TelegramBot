from aiogram import executor, types
from aiogram.dispatcher import FSMContext

import database.crud.operator
import serializator
from database.crud.order import OrderClass
from database.crud.operator import OperatorClass
from keyboard.keyboard import default_cities
from state.operator_state import StateOperator
from state.state import register_handlers, StateOrder
from config import dp, bot

register_handlers(dp)

@dp.message_handler(commands=['start'],  state=None)
async def send_welcome(message: types.Message):
    await message.reply("Привет! Город откуда хотите переслать:", reply_markup=default_cities)
    await StateOrder.city_from.set()

#-------------------------------------------------------------------------


@dp.callback_query_handler()
async def on_inline_button(callback_query: types.CallbackQuery, state: FSMContext):
    cart = callback_query.data.split(':')

    match cart[0]:
        case 'accept_id':
            async with state.proxy() as data:
                data['id_order'] = cart[3]

            await StateOperator.get_rate.set()
            database.crud.order.OrderClass().update_order(id=cart[3],
                                                          telegram_id_operator=callback_query.message.chat.id)
            database.crud.operator.OperatorClass().update_operator(id_telegram_op=callback_query.message.chat.id)
            await callback_query.message.reply(
                f"Вы приняли заказ!\n{serializator.ser(OrderClass().one_order(id=cart[3]))}"
                f"\n\nСейчас напишите курс:")

        case 'cancel_id':
            await callback_query.message.reply(f"Вы отказали: Имя: {cart[1]}, id_telegram:{cart[2]}\nОн будет проинформирован")
            await bot.send_message(cart[2], "Твой заказ отклонен!")

        case 'client_accept_id':
            await bot.send_message(cart[2], "Твой заказ принят! Жди сообщение с подскасками.")
            await bot.send_message(database.crud.operator.OperatorClass().one_operator(1).id_telegram_op, f"Клиент {cart[3]} согласился.")

        case 'client_cancel_id':
            await bot.send_message(cart[2], "Хорошо!")
            await bot.send_message(database.crud.operator.OperatorClass().one_operator(1).id_telegram_op, f"Клиент {cart[3]} отказался.")

        case _:
            return None

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id) #delete sms with buttons


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
