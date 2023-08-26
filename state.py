from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode

import check_text
import database.crud.order
from config import dp, bot, w_another, w_cancel, w_another_ag
from keyboard.inline_buttons import get_inline_keyboard
from keyboard.keyboard import another_rm, main_but, start_key, default_cities, h_curr_all, view_money, how_surr, how_curr_add, to_city, h_curr_a, non_cash


class StateOrder(StatesGroup):
    city_from = State()
    curr_set = State()
    total = State()
    city_to = State()
    curr_get = State()
    view_money = State()


@dp.message_handler(state=StateOrder.city_from)
async def get_city_from(message: types.Message, state: FSMContext):
    await check_text.check_text(message, StateOrder.city_from, StateOrder.curr_set, h_curr_all, state, "Напишите город либо выберите из списка:", "В какой валютe:" , "city_from")


@dp.message_handler(state=StateOrder.curr_set)
async def get_curr_set(message: types.Message, state: FSMContext):
    await check_text.check_text(message=message, current_state=StateOrder.curr_set, next_state=StateOrder.total, reply_mark=main_but, state=state, text_another='Напишите валюту либо выберите из списка', success_text="Сумма:", key='curr_set', add=h_curr_a)


@dp.message_handler(state=StateOrder.total)
async def get_total(message: types.Message, state: FSMContext):
    await check_text.check_text(message=message, current_state=StateOrder.total, next_state=StateOrder.city_to,
                                reply_mark=to_city, state=state, text_another='Напишите сумму:',
                                success_text="В какой город:", key='total')


@dp.message_handler(state=StateOrder.city_to)
async def get_city_to(message: types.Message, state: FSMContext):
    await check_text.check_text(message=message, current_state=StateOrder.city_to, next_state=StateOrder.curr_get,
                                reply_mark=how_surr, state=state, text_another='Напишите город либо выберите из списка:',
                                success_text="В какой валюте получить:", key='city_to')


@dp.message_handler(state=StateOrder.curr_get)
async def get_curr_get(message: types.Message, state: FSMContext):
    await check_text.check_text(message=message, current_state=StateOrder.curr_get, next_state=StateOrder.view_money,
                                reply_mark=view_money, state=state, text_another='Напишите город либо выберите из списка:',
                                success_text="Напишите в каком виде хотите получить:", key='curr_get', add=how_curr_add)


@dp.message_handler(state=StateOrder.view_money)
async def get_view_money(message: types.Message, state: FSMContext):
    if message.text == str(w_another):
        await bot.send_message(message.chat.id, f"Напишите в каком виде хотите получить")
        await StateOrder.view_money.set()

    elif message.text == str(w_cancel):
        await state.finish()

    elif message.text == 'Безналичные':
        await bot.send_message(message.chat.id, f"На какое лицо:", reply_markup=non_cash)
        await StateOrder.view_money.set()

    else:
        if message.text == 'Юридичесское лицо':
            message.text = 'Юридичесское лицо. Безналичные'
        elif message.text == 'Физичесское лицо':
            message.text = 'Физичесское лицо. Безналичные'

        async with state.proxy() as data:
            data['view_money'] = message.text

        try:
            async with state.proxy() as data:
                await bot.send_message(message.chat.id, f"<i>Откуда:</i> {data['city_from']}\n"
                                                        f"<i>В какой валюте:</i> {data['curr_set']}\n"
                                                        f"<i>Сумма:</i> {data['total']}\n"
                                                        f"<i>В какой город:</i> {data['city_to']}\n"
                                                        f"<i>В какой валюте:</i> {data['curr_get']}\n"
                                                        f"<i>В каком виде:</i> {data['view_money']}\n",
                                    reply_markup=start_key, parse_mode=ParseMode.HTML)
            #save data client
            database.crud.order.OrderClass().store_order(telegram_id=message.chat.id,
                                                         name_client=message.from_user.first_name,
                                                         is_accept_op=False, is_accept_client=False,
                                                         city_from=data['city_from'], curr_set=data['curr_set'],
                                                         total=data['total'], city_to=data['city_to'],
                                                         curr_get=data['curr_get'], view_money=data['view_money'])

            operator = database.crud.operator.OperatorClass().one_operator(1)
            user = database.crud.order.OrderClass().one_order(telegram_id=message.chat.id)

            from keyboard.inline_buttons import button_select_oper
            await bot.send_message(chat_id=operator.id_telegram_op, text=user, reply_markup=get_inline_keyboard(user.telegram_id, user.name_client)) #send message to operator
        except Exception as ex:
            print(ex)
        finally:
            await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_city_from, content_types=['text'], state=StateOrder.city_from)
    dp.register_message_handler(get_curr_set, content_types=['text'], state=StateOrder.curr_get)
    dp.register_message_handler(get_total, content_types=['text'], state=StateOrder.total)
    dp.register_message_handler(get_city_to, content_types=['text'], state=StateOrder.city_to)
    dp.register_message_handler(get_curr_get, content_types=['text'], state=StateOrder.curr_get)
    dp.register_message_handler(get_view_money, content_types=['text'], state=StateOrder.view_money)
