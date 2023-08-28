from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from forms.functions_c import Functions
import api_sheet
import database.crud.operator
import serializator
from database.crud.order import OrderClass
from database.crud.operator import OperatorClass
from keyboard.inline_form import send_paginated_buttons

from forms.operator_state import StateOperator
from config import dp, bot, n


@dp.message_handler(commands=['start'],  state=None)
async def send_welcome(message: types.Message, state: FSMContext):
    n['actual_question'] = 0
    global buttons_api
    buttons_api = api_sheet.main()
    await Functions().send_city_from(message.chat.id)


@dp.callback_query_handler()
async def on_inline_button(callback_query: types.CallbackQuery, state: FSMContext):
    cart = callback_query.data.split(':')

    match cart[0]:
        case 'button':
            delete_f = await bot.delete_message(chat_id=callback_query.message.chat.id,
                                                message_id=callback_query.message.message_id)
            button_text = callback_query.data.split(':')[1]
            print(cart)
            n[f'{button_text}'] = button_text
            functions = Functions()

            if n['actual_question'] == 0:
                delete_f
                n['actual_question'] = 1
                await functions.send_currency(callback_query.message.chat.id)
            elif n['actual_question'] == 1:
                delete_f
                n['actual_question'] = 2
                await functions.send_total(callback_query.message.chat.id)
            elif n['actual_question'] == 2:
                delete_f
                n['actual_question'] = 3
                await functions.send_currency_to(callback_query.message.chat.id)
            elif n['actual_question'] == 3:
                delete_f
                n['actual_question'] = -1
                await functions.send_currency_view(callback_query.message.chat.id)
            elif n['actual_question'] == -1:
                await bot.send_message(callback_query.message.chat.id, f"Все записано!")


        case 'next_page':
            global buttons_api
            keyboard = send_paginated_buttons(page=int(callback_query.data.split(':')[1]),
                                              number_cell=int(callback_query.data.split(':')[2]),
                                              button_list_domestic=buttons_api)
            await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                                reply_markup=keyboard)

        case 'accept_id':
            async with state.proxy() as data:
                data['id_order'] = cart[3]

            if database.crud.order.OrderClass().one_order(id=cart[3]).telegram_id_operator == None:
                await StateOperator.get_rate.set()
                database.crud.order.OrderClass().update_order(id=cart[3],
                                                              telegram_id_operator=callback_query.message.chat.id)
                database.crud.operator.OperatorClass().update_operator(id_telegram_op=callback_query.message.chat.id)
                await callback_query.message.reply(
                    f"Вы приняли заявку!\n{serializator.ser(OrderClass().one_order(id=cart[3]))}"
                    f"\n\nСейчас напишите курс:")
            else:
                await bot.send_message(callback_query.message.chat.id, 'Заявка уже оброблена!')

        case 'cancel_id':
            if database.crud.order.OrderClass().one_order(id=cart[3]).telegram_id_operator is None:
                database.crud.order.OrderClass().update_order(id=cart[3],
                                                              telegram_id_operator=callback_query.message.chat.id)
                await callback_query.message.reply(f"Вы отказали: Имя: {cart[1]}, id_telegram:{cart[2]}\nОн будет проинформирован")
                await bot.send_message(cart[2], "Твоя заявка отклонен!")
            else:
                await bot.send_message(callback_query.message.chat.id, 'Заявка уже оброблена!')

        case 'client_accept_id':
            await bot.send_message(cart[2], "Твоя заявка принят! Жди сообщение с подскасками.")
            await bot.send_message(database.crud.order.OrderClass().one_order(id=cart[1]).telegram_id_operator, f"Клиент {cart[3]} согласился.")

        case 'client_cancel_id':
            await bot.send_message(cart[2], "Хорошо!")
            await bot.send_message(database.crud.order.OrderClass().one_order(id=cart[1]).telegram_id_operator, f"Клиент {cart[3]} отказался.")
        case _:
                return None

    ####delete here


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
            await send_paginated_buttons(message.chat.id, page=1)
        case 'api':
            print(api_sheet.main())
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
