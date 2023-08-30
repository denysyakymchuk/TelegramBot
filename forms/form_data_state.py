from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import dp,  n
from forms.functions_c import Functions, StateTotal
from tools import send_message_to_operators


class GetFormDataState(StatesGroup):
    get_option_city_from = State()
    get_option_currently_from = State()
    get_option_city_to = State()
    get_option_currently_to = State()


@dp.message_handler(state=GetFormDataState.get_option_city_from)
async def get_option_city_from(message: types.Message, state: FSMContext):
        try:
                n['key_city'] = None
                n['city_from'] = message.text
                await state.finish()
                await Functions().send_currency(message.chat.id, selected_city=message.text)

        except Exception as error:
            from logconfig import setup_logging
            logger = setup_logging()
            logger.error(f"{error}")


@dp.message_handler(state=GetFormDataState.get_option_currently_from)
async def get_option_currently_from(message: types.Message, state: FSMContext):
        try:
                n['key_city'] = None
                n['curr_set'] = message.text
                await state.finish()
                await message.reply("Напиши сумму:")
                await StateTotal.get_total.set()

        except Exception as error:
            from logconfig import setup_logging
            logger = setup_logging()
            logger.error(f"{error}")


@dp.message_handler(state=GetFormDataState.get_option_city_to)
async def get_option_city_to(message: types.Message, state: FSMContext):
        try:
                n['key_city'] = None
                n['actual_question'] = -1
                n['city_to'] = message.text
                await state.finish()
                await Functions().send_currency_to(message.chat.id, selected_city='')

        except Exception as error:
            from logconfig import setup_logging
            logger = setup_logging()
            logger.error(f"{error}")


@dp.message_handler(state=GetFormDataState.get_option_currently_to)
async def get_option_currently_to(message: types.Message, state: FSMContext):
        try:
                n['actual_question'] = 0
                n['key_city'] = None
                n['curr_get'] = message.text
                await state.finish()
                await send_message_to_operators(message.chat.first_name)

        except Exception as error:
            from logconfig import setup_logging
            logger = setup_logging()
            logger.error(f"{error}")
