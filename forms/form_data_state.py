from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import dp, get_keyboard, n
from forms.functions_c import Functions, StateTotal


class GetFormDataState(StatesGroup):
    get_option_city_from = State()
    get_option_currently_from = State()
    get_option_city_to = State()
    get_option_currently_to = State()


@dp.message_handler(state=GetFormDataState.get_option_city_from)
async def get_option_city_from(message: types.Message, state: FSMContext):
        n['key_city'] = None
        n['actual_question'] = 1
        await state.finish()
        await Functions().send_currency(message.chat.id, selected_city=message.text)


@dp.message_handler(state=GetFormDataState.get_option_currently_from)
async def get_option_currently_from(message: types.Message, state: FSMContext):
        n['key_city'] = None
        n['actual_question'] = 2
        await state.finish()
        await message.reply("Напиши сумму:")
        await StateTotal.get_total.set()


@dp.message_handler(state=GetFormDataState.get_option_city_to)
async def get_option_city_to(message: types.Message, state: FSMContext):
        print('SUCCESS')
        n['key_city'] = None
        n['actual_question'] = 2
        await state.finish()
        await Functions().send_city_to(message.chat.id)

