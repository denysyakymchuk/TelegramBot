from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import database.crud.operator
from config import dp, bot
from keyboard.inline_buttons import get_user_im_responce


class StateOperator(StatesGroup):
    get_rate = State()
    get_deadline = State()


@dp.message_handler(state=StateOperator.get_rate)
async def get_city_from(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(message.chat.id, "Введите пожалуста сроки и другую важную информацию:")
        await StateOperator.get_deadline.set()
    except Exception as ex:
        from write_logs import write_logs
        write_logs.write_logs(ex)
        await state.finish()


@dp.message_handler(state=StateOperator.get_deadline)
async def get_city_from(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['get_deadline'] = message.text

        from database.crud.order import OrderClass

        user_model = OrderClass().update_order(id=data['id_order'], is_accept_op=True, reply_message=str("Курс: " + data['get_rate'] + " \n" + "Сроки: " + data["get_deadline"]))
        await bot.send_message(user_model.telegram_id_operator, f"Сообщение отправлено!")
        await bot.send_message(user_model.telegram_id, f"Твой заказ принят!\n {user_model.reply_message}", reply_markup=get_user_im_responce(user_model))

    except Exception as ex:
        from write_logs import write_logs
        write_logs(ex)
    finally:
        await state.finish()


