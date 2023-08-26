from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_accept_client = InlineKeyboardButton(text="Принять", callback_data='accept_client')
button_cancel_client = InlineKeyboardButton(text="Отказать", callback_data='cancel_client')
button_select_client = InlineKeyboardMarkup().add(button_accept_client, button_accept_client)

button_accept_oper = InlineKeyboardButton(text="Принять", callback_data='accept_oper')
button_cancel_oper = InlineKeyboardButton(text="Отказать", callback_data='cancel_oper')
button_select_oper = InlineKeyboardMarkup().add(button_accept_oper, button_cancel_oper)

button_spam_text = InlineKeyboardButton(text="Ответ отправлен", callback_data='spam')
button_spam = InlineKeyboardMarkup().add(button_spam_text)


def get_inline_keyboard(telegram_id, name_client):
    inline_kb = InlineKeyboardMarkup()
    print(telegram_id)
    button_accept_operator = InlineKeyboardButton(
        text="Accept",
        callback_data=f"accept_id:{name_client}:{telegram_id}"  # Передаем аргумент в callback_data
    )
    button_cancel_operator = InlineKeyboardButton(
        text='Cancel',
        callback_data=f'cancel_id:{name_client}:{telegram_id}'
    )
    print(button_cancel_operator.callback_data)
    print(button_accept_operator.callback_data)
    inline_kb.add(button_accept_operator, button_cancel_operator)
    return inline_kb