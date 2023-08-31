import loguru
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


from config import dp,  n
from forms.functions_c import Functions, StateTotal
from serializator import contains_digits
from tools import send_message_to_operators


class GetFormDataState(StatesGroup):
    get_option_city_from = State()
    get_option_currently_from = State()
    get_option_city_to = State()
    get_option_currently_to = State()


@dp.message_handler(state=GetFormDataState.get_option_city_from)
async def get_option_city_from(message: types.Message, state: FSMContext):
        try:
            if contains_digits(message.text):
                await message.reply("Must be only letters! Try again")
                loguru.logger.info(f'No valid sending from city - {message.text}')

                await GetFormDataState.get_option_city_from.set()
            else:
                n['key_city'] = None
                n['city_from'] = message.text
                await state.finish()
                loguru.logger.info(f'Enter sending from city - {message.text}')
                await Functions().send_currency(message.chat.id, selected_city=message.text)

        except Exception as error:
            await state.finish()
            loguru.logger.error(error)


@dp.message_handler(state=GetFormDataState.get_option_currently_from)
async def get_option_currently_from(message: types.Message, state: FSMContext):
        try:
            if contains_digits(message.text):
                await message.reply("Must be only letters! Try again")
                loguru.logger.info(f'No valid sending currency - {message.text}')
                await GetFormDataState.get_option_currently_from.set()
            else:
                n['key_city'] = None
                n['curr_set'] = message.text
                await state.finish()
                await message.reply("Enter the amount:")
                loguru.logger.info(f'Enter sending currency - {message.text}')
                await StateTotal.get_total.set()

        except Exception as error:
            await state.finish()
            loguru.logger.critical(error)


@dp.message_handler(state=GetFormDataState.get_option_city_to)
async def get_option_city_to(message: types.Message, state: FSMContext):
        try:
            if contains_digits(message.text):
                await message.reply("Must be only letters! Try again")
                loguru.logger.info(f'No valid sending to city - {message.text}')
                await GetFormDataState.get_option_city_to.set()
            else:
                n['key_city'] = None
                n['actual_question'] = -1
                n['city_to'] = message.text
                await state.finish()
                loguru.logger.info(f'Enter sending to city - {message.text}')
                await Functions().send_currency_to(message.chat.id, selected_city='')

        except Exception as error:
            await state.finish()
            loguru.logger.critical(error)


@dp.message_handler(state=GetFormDataState.get_option_currently_to)
async def get_option_currently_to(message: types.Message, state: FSMContext):
        try:
            if contains_digits(message.text):
                await message.reply("Must be only letters! Try again")
                loguru.logger.info(f'No valid receving currency - {message.text}')
                await GetFormDataState.get_option_currently_to.set()
            else:
                n['actual_question'] = 0
                n['key_city'] = None
                n['curr_get'] = message.text
                await state.finish()
                loguru.logger.info(f'Enter receving currency - {message.text}')
                await send_message_to_operators(message.chat.first_name)

        except Exception as error:
            await state.finish()
            loguru.logger.critical(error)

