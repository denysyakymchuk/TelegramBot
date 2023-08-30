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
                                                     curr_get=n['curr_get'], view_money=None)
        actual_order = OrderClass().one_order(telegram_id=n['id_th'], city_from=n['city_from'],
                                                                  curr_set=n['curr_set'], total=n['total'],
                                                                  city_to=n['city_to'], curr_get=n['curr_get'],
                                                                  view_money=None)
        operators = serializator.get_operators_from_sheet(get_keyboard())

        for operator in operators:
            await bot.send_message(operator, serializator.ser(actual_order),
                                   reply_markup=get_inline_keyboard(actual_order))
    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")