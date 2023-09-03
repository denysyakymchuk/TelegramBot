import asyncio
import threading
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from telethon import TelegramClient
from telethon.tl.functions.channels import GetAdminLogRequest
from telethon.tl.types import ChannelAdminLogEventsFilter
import json
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

client = TelegramClient('session.session', config.api_id, config.api_hash)


async def process_recent_actions():
    try:
        input_channel = tools.get_channel_name(get_keyboard())
        id = await client.get_entity(input_channel)
        print(id)
        n["id_channel"] = id.id
        message = tools.get_message(get_keyboard())
        events_filter = ChannelAdminLogEventsFilter(
            join=True,
        )
        admin_log = await client(GetAdminLogRequest(
            channel=input_channel,
            q='',
            max_id=0,
            min_id=0,
            limit=10,
            events_filter=events_filter
        ))
        with open("users.json", 'r') as json_file:
            data = json.load(json_file)

        for id_user in admin_log.events:
            if not any(id_user.id == entry.get("id") for entry in data):
                print('NEW')
                await client.send_message(id_user.user_id, message)
                new_data = {
                    "id": id_user.id,
                    "user_id": id_user.user_id,
                }
                data.append(new_data)
            else:
                pass

        with open("users.json", 'w') as json_file:
            json_file.write(json.dumps(data, indent=4))

    except Exception as e:
        logger.critical(e)
        time.sleep(600)


async def run_client():
    try:
        await client.start(bot_token=config.TOKEN)
        while True:
            print("One iteration")
            await process_recent_actions()
            time.sleep(600)

    except Exception as error:
        logger.critical(error)


async def is_user_subscribed(user_id):
    try:
        print(n["id_channel"])
        chat_member = await bot.get_chat_member(int('-100'+str(n["id_channel"])), user_id)
        return chat_member.is_chat_member()
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False


@dp.message_handler(commands=['start'], state=None)
async def send_welcome(message: types.Message):
    try:
        if await is_user_subscribed(message.chat.id):
            logger.info(f'/start user  - {message.chat.id}')
            n['actual_question'] = 0
            get_keyboard(load=True)
            await Functions().send_city_from(message.chat.id)
        else:
            await message.reply(f"You can not use this bot!")

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
                    logger.info('Select city sending from')
                    await bot.delete_message(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id)
                    n['actual_question'] = 1
                    await functions.send_currency(callback_query.message.chat.id, button_text)
                elif n['actual_question'] == 1:
                    n['curr_set'] = cart[1]
                    logger.info('Select sending currency')
                    await bot.delete_message(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id)
                    n['actual_question'] = 2
                    await functions.send_total(callback_query.message.chat.id)
                elif n['actual_question'] == 2:
                    n['city_to'] = cart[1]
                    await bot.delete_message(chat_id=callback_query.message.chat.id,
                                             message_id=callback_query.message.message_id)
                    logger.info('Select city sending to')
                    n['actual_question'] = -1
                    await functions.send_currency_to(callback_query.message.chat.id, button_text)
                elif n['actual_question'] == -1:
                    n['curr_get'] = cart[1]
                    logger.info('Select currency receiving')
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
                    await bot.send_message(callback_query.message.chat.id, "Write from which city")
                    await GetFormDataState.get_option_city_from.set()
                elif int(cart[2]) == 1:
                    n['actual_question'] = 2
                    await bot.send_message(callback_query.message.chat.id, "Write in which currency")
                    await GetFormDataState.get_option_currently_from.set()
                elif int(cart[2]) == 2:
                    n['actual_question'] = 3
                    await bot.send_message(callback_query.message.chat.id, "Write in which city")
                    await GetFormDataState.get_option_city_to.set()
                elif int(cart[2]) == 3:
                    n['actual_question'] = -1
                    await bot.send_message(callback_query.message.chat.id, "Write in which currency':")
                    await GetFormDataState.get_option_currently_to.set()

            case 'accept_id':
                async with state.proxy() as data:
                    data['id_order'] = cart[3]

                if database.crud.order.OrderClass().one_order(id=cart[3]).telegram_id_operator == None:
                    logger.info('Request accepted from operator')
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
                    await callback_query.message.reply(
                        f"Canceled: Username: {cart[1]}, Telegram id:{cart[2]}\nHe will informed!")
                    await bot.send_message(cart[2],
                                           "Our apologies, but we are not able to fulfill your request at the moment!")
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
                await bot.send_message(database.crud.order.OrderClass().one_order(id=cart[1]).telegram_id_operator,
                                       f"Клиент {cart[3]} согласился.")
                logger.info('Request accepted from client')

            case 'client_cancel_id':
                await bot.delete_message(chat_id=callback_query.message.chat.id,
                                         message_id=callback_query.message.message_id)
                await bot.send_message(cart[2], "Okey!")
                await bot.send_message(database.crud.order.OrderClass().one_order(id=cart[1]).telegram_id_operator,
                                       f"Клиент {cart[3]} отказался.")
                logger.info('Request canceled from client')
            case _:
                pass

    except Exception as error:
        logger.critical(error)


if __name__ == '__main__':
    try:
        print(get_keyboard(load=True))
        init_csv_logger()
        client_thread = threading.Thread(target=lambda: asyncio.run(run_client()))
        client_thread.start()
        executor.start_polling(dp, skip_updates=True)

    except Exception as error:
        logger.critical(error)
