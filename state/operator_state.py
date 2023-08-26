from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import dp, bot, id_keys


class StateOperator(StatesGroup):
    get_rate = State()
    get_deadline = State()


@dp.message_handler(state=StateOperator.get_rate)
async def get_city_from(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['get_rate'] = message.text
        await bot.send_message(message.chat.id, "Введите пожалуста сроки и другую информацию:")
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

        OrderClass().update_order(id=data['id_order'], is_accept_op=True, reply_message=str("Курс: " + data['get_rate'] + " | " + "Сроки: " + data["get_deadline"]))
        await bot.send_message()
    except Exception as ex:
        from write_logs import write_logs
        write_logs(ex)
    finally:
        await state.finish()



