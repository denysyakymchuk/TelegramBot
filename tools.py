import loguru

import serializator
from config import bot, n, get_keyboard
from database.crud.order import OrderClass
from keyboard.inline_buttons import get_inline_keyboard


async def send_message_to_operators(name_client):
    try:
        await bot.send_message(n['id_th'], f"Got it!\n\n{serializator.view_json_output(n)}")
        OrderClass().store_order(telegram_id=n['id_th'],
                                                     name_client=name_client,
                                                     is_accept_client=False, is_accept_op=False, city_from=n['city_from'],
                                                     curr_set=n['curr_set'], total=n['total'], city_to=n['city_to'],
                                                     curr_get=n['curr_get']
                                 )
        actual_order = OrderClass().one_order(telegram_id=n['id_th'], city_from=n['city_from'],
                                                                  curr_set=n['curr_set'], total=n['total'],
                                                                  city_to=n['city_to'], curr_get=n['curr_get']
                                                                  )
        operators = serializator.get_operators_from_sheet(get_keyboard())

        for operator in operators:
            try:
                await bot.send_message(operator, serializator.ser(actual_order),
                                       reply_markup=get_inline_keyboard(actual_order))
            except:
                loguru.logger.error(f"No send message to operator - {operator}")

    except Exception as error:
        loguru.logger.critical(error)


async def send_message_to_admins(message):
    admins = serializator.get_admins_from_sheet()

    for admin in admins:
        try:
            await bot.send_message(admin, message)
        except:
            loguru.logger.error(f"No send message to admin -  {admin}")