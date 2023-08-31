import csv

import loguru
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

import config
import tools
from forms.form_data_state import GetFormDataState
from forms.functions_c import Functions
import database.crud
import serializator
from database.crud.order import OrderClass
from keyboard.inline_form import send_paginated_buttons

from forms.operator_state import StateOperator
from config import dp, bot, n, get_keyboard
from loguru import logger

from logconfig import init_csv_logger

logger.add("logs.csv", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")


@dp.message_handler(commands=['start'],  state=None)
async def send_welcome(message: types.Message):
    try:
        logger.info(f'/start user  - {message.chat.id}')
        n['actual_question'] = 0
        get_keyboard(load=True)
        await Functions().send_city_from(message.chat.id)

    except Exception as error:
        logger.critical(error)


@dp.callback_query_handler()
async def on_inline_button(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        cart = callback_query.data.split(':')

        match cart[0]:
            case 'button':
                button_text = callback_query.data.split(':')[1]
                functions = Functions()

                if n['actual_question'] == 0:
                    n['city_from'] = cart[1]
                    await bot.delete_message(chat_id=callback_query.message.chat.id,
                                                        message_id=callback_query.message.message_id)
                    n['actual_question'] = 1
                    await functions.send_currency(callback_query.message.chat.id, button_text)
                elif n['actual_question'] == 1:
                    n['curr_set'] = cart[1]
                    await bot.delete_message(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id)
                    n['actual_question'] = 2
                    await functions.send_total(callback_query.message.chat.id)
                elif n['actual_question'] == 2:
                    n['city_to'] = cart[1]
                    await bot.delete_message(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id)
                    n['actual_question'] = -1
                    await functions.send_currency_to(callback_query.message.chat.id, button_text)
                elif n['actual_question'] == -1:
                    n['curr_get'] = cart[1]
                    await bot.delete_message(chat_id=callback_query.message.chat.id,
                                                        message_id=callback_query.message.message_id)
                    n['key_city'] = None
                    await tools.send_message_to_operators(callback_query.message.chat.first_name)

            case 'next_page':
                keyboard = send_paginated_buttons(page=int(callback_query.data.split(':')[1]),
                                                  number_cell=int(callback_query.data.split(':')[2]),
                                                  button_list_domestic=config.get_keyboard(), is_city=n['key_city'])

                await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                                    reply_markup=keyboard)
                logger.info('Next page')
            case 'prev_page':
                keyboard = send_paginated_buttons(page=int(callback_query.data.split(':')[1]),
                                                  number_cell=int(callback_query.data.split(':')[2]),
                                                  button_list_domestic=get_keyboard(), is_city=n['key_city'])
                await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                                    reply_markup=keyboard)
                logger.info('Preview page')

            case 'add_option':
                logger.info('Pressed custom button')
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)

                if int(cart[2]) == 0:
                    n['actual_question'] = 1
                    await bot.send_message(callback_query.message.chat.id, "Напиши с какого города:")
                    await GetFormDataState.get_option_city_from.set()
                elif int(cart[2]) == 1:
                    n['actual_question'] = 2
                    await bot.send_message(callback_query.message.chat.id, "Напиши в какой валюте:")
                    await GetFormDataState.get_option_currently_from.set()
                elif int(cart[2]) == 2:
                    n['actual_question'] = 3
                    await bot.send_message(callback_query.message.chat.id, "Напиши в какой город:")
                    await GetFormDataState.get_option_city_to.set()
                elif int(cart[2]) == 3:
                    n['actual_question'] = -1
                    await bot.send_message(callback_query.message.chat.id, "Напиши в какой валюте:")
                    await GetFormDataState.get_option_currently_to.set()

            case 'accept_id':
                async with state.proxy() as data:
                    data['id_order'] = cart[3]

                ###
                if database.crud.order.OrderClass().one_order(id=cart[3]).telegram_id_operator == None:
                    logger.info('Request accepted from operator')
                    ###
                    await StateOperator.get_rate.set()
                    database.crud.order.OrderClass().update_order(id=cart[3],
                                                                  telegram_id_operator=callback_query.message.chat.id)

                    await callback_query.message.reply(
                        f"Accepted!\n{serializator.ser(OrderClass().one_order(id=cart[3]))}"
                        f"\n\nСейчас напишите курс:")
                else:
                    await bot.send_message(callback_query.message.chat.id, 'Заявка уже оброблена!')
                    logger.info('Request already accepted')
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)

            case 'cancel_id':
                if database.crud.order.OrderClass().one_order(id=cart[3]).telegram_id_operator is None:
                    database.crud.order.OrderClass().update_order(id=cart[3],
                                                                  telegram_id_operator=callback_query.message.chat.id)
                    await callback_query.message.reply(f"Canceled: Username: {cart[1]}, Telegram id:{cart[2]}\nHe will informed!")
                    await bot.send_message(cart[2], "Our apologies, but we are not able to fulfill your request at the moment!")
                    logger.info('Request canceled from operator')
                else:
                    await bot.send_message(callback_query.message.chat.id, 'Заявка уже оброблена!')
                    logger.info('Request already accepted from operator')
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)

            case 'client_accept_id':
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)
                await bot.send_message(cart[2], "Your request has been accepted.")
                order = database.crud.order.OrderClass().update_order(id=cart[1], is_accept_client=True)
                await tools.send_message_to_admins(serializator.ser(order))
                await bot.send_message(database.crud.order.OrderClass().one_order(id=cart[1]).telegram_id_operator, f"Клиент {cart[3]} согласился.")
                logger.info('Request accepted from client')

            case 'client_cancel_id':
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)
                await bot.send_message(cart[2], "Okey!")
                await bot.send_message(database.crud.order.OrderClass().one_order(id=cart[1]).telegram_id_operator, f"Клиент {cart[3]} отказался.")
                logger.info('Request canceled from client')
            case _:
                pass

    except Exception as error:
        logger.critical(error)


if __name__ == '__main__':
    init_csv_logger()
    executor.start_polling(dp, skip_updates=True)
