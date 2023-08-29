from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import serializator
from config import dp, get_keyboard, n, bot
from database import database
from database.crud.operator import OperatorClass
from database.crud.order import OrderClass
from forms.functions_c import Functions, StateTotal
from keyboard.inline_buttons import get_user_im_responce, get_inline_keyboard
from serializator import view_json_output


class GetFormDataState(StatesGroup):
    get_option_city_from = State()
    get_option_currently_from = State()
    get_option_city_to = State()
    get_option_currently_to = State()


@dp.message_handler(state=GetFormDataState.get_option_city_from)
async def get_option_city_from(message: types.Message, state: FSMContext):
        n['key_city'] = None
        n['city_from'] = message.text
        await state.finish()
        await Functions().send_currency(message.chat.id, selected_city=message.text)


@dp.message_handler(state=GetFormDataState.get_option_currently_from)
async def get_option_currently_from(message: types.Message, state: FSMContext):
        n['key_city'] = None
        n['curr_set'] = message.text
        await state.finish()
        await message.reply("Напиши сумму:")
        await StateTotal.get_total.set()


@dp.message_handler(state=GetFormDataState.get_option_city_to)
async def get_option_city_to(message: types.Message, state: FSMContext):
        n['key_city'] = None
        n['actual_question'] = -1
        n['city_to'] = message.text
        await state.finish()
        await Functions().send_currency_to(message.chat.id, selected_city='')


@dp.message_handler(state=GetFormDataState.get_option_currently_to)
async def get_option_currently_to(message: types.Message, state: FSMContext):
        print('SUCCESS')
        n['key_city'] = None
        n['actual_question'] = 0
        n['curr_get'] = message.text
        await state.finish()
        await message.reply(f'Got it!\n\n{view_json_output(n)}')
        OrderClass().store_order(telegram_id=n['id_th'],
                                                     name_client=message.chat.first_name,
                                                     is_accept_client=False, is_accept_op=False,
                                                     city_from=n['city_from'], curr_set=n['curr_set'], total=n['total'],
                                                     city_to=n['city_to'], curr_get=n['curr_get'], view_money=None)
        b = OrderClass().one_order(telegram_id=n['id_th'], city_from=n['city_from'],
                                                       curr_set=n['curr_set'], total=n['total'], city_to=n['city_to'],
                                                       curr_get=n['curr_get'], view_money=None)
        print(b)
        await bot.send_message(OperatorClass().one_operator(1).id_telegram_op, serializator.ser(b),
                               reply_markup=get_inline_keyboard(b))

