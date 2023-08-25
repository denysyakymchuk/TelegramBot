from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode

from config import dp, bot


class StateOrder(StatesGroup):
    city_from = State()
    curr_set = State()
    total = State()
    city_to = State()
    curr_get = State()
    view_money = State()


@dp.message_handler(state=StateOrder.city_from)
async def get_city_from(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city_from'] = message.text

    await bot.send_message(message.chat.id, "Отлично!\nТеперь в какой валюте:")
    await StateOrder.curr_set.set()


@dp.message_handler(state=StateOrder.curr_set)
async def get_curr_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['curr_set'] = message.text

    await bot.send_message(message.chat.id, "Отлично!\nТеперь сумма:")
    await StateOrder.total.set()


@dp.message_handler(state=StateOrder.total)
async def get_total(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['total'] = message.text

    await bot.send_message(message.chat.id, "Отлично!\nСейчас город в какой нужно переслать:")
    await StateOrder.city_to.set()


@dp.message_handler(state=StateOrder.city_to)
async def get_city_to(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city_to'] = message.text

    await bot.send_message(message.chat.id, "Отлично! Сейчас в какой валюте получить:")
    await StateOrder.curr_get.set()


@dp.message_handler(state=StateOrder.curr_get)
async def get_curr_get(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['curr_get'] = message.text

    await bot.send_message(message.chat.id, "Отлично! Сейчас в каком виде получить:")
    await StateOrder.view_money.set()


@dp.message_handler(state=StateOrder.view_money)
async def get_view_money(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['view_money'] = message.text

    async with state.proxy() as data:
        await bot.send_message(message.chat.id, f"Отлично!\n\n<i>Откуда:</i> {data['city_from']}\n"
                                                f"<i>В какой валюте:</i> {data['curr_set']}\n"
                                                f"<i>Сумма:</i> {data['total']}\n"
                                                f"<i>В какой город:</i> {data['city_to']}\n"
                                                f"<i>В какой валюте:</i> {data['curr_get']}\n"
                                                f"<i>В каком виде:</i> {data['view_money']}\n", parse_mode=ParseMode.HTML)

    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_city_from, content_types=['text'], state=StateOrder.city_from)
    dp.register_message_handler(get_curr_set, content_types=['text'], state=StateOrder.curr_get)
    dp.register_message_handler(get_total, content_types=['text'], state=StateOrder.total)
    dp.register_message_handler(get_city_to, content_types=['text'], state=StateOrder.city_to)
    dp.register_message_handler(get_curr_get, content_types=['text'], state=StateOrder.curr_get)
    dp.register_message_handler(get_view_money, content_types=['text'], state=StateOrder.view_money)
