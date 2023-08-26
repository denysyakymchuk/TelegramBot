from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_accept_client = InlineKeyboardButton(text="Принять", callback_data='accept_client')
button_cancel_client = InlineKeyboardButton(text="Отказать", callback_data='cancel_client')
button_select_client = InlineKeyboardMarkup().add(button_accept_client, button_accept_client)

button_spam_text = InlineKeyboardButton(text="Ответ отправлен", callback_data='spam')
button_spam = InlineKeyboardMarkup().add(button_spam_text)


def get_inline_keyboard(user):
    button_accept_operator = InlineKeyboardButton(
        text="Accept",
        callback_data=f"accept_id:{user.name_client}:{user.telegram_id}:{user.id}"  # Передаем аргумент в callback_data
    )
    button_cancel_operator = InlineKeyboardButton(
        text='Cancel',
        callback_data=f'cancel_id:{user.name_client}:{user.telegram_id}:{user.id}'
    )
    inline_kb = InlineKeyboardMarkup().add(button_accept_operator, button_cancel_operator)
    return inline_kb


def get_user_im_responce(user):
    button_accept_client = InlineKeyboardButton(
        text="Согласиться",
        callback_data=f"client_accept_id:{user.id}:{user.telegram_id}:{user.name_client}"  # Передаем аргумент в callback_data
    )
    button_cancel_client = InlineKeyboardButton(
        text='Отказаться',
        callback_data=f'client_cancel_id:{user.id}:{user.telegram_id}:{user.name_client}'
    )
    inline_kb_client = InlineKeyboardMarkup().add(button_accept_client, button_cancel_client)
    return inline_kb_client