from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_inline_keyboard(user):
    try:
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

    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")


def get_user_im_responce(user):
    try:
        button_accept_client = InlineKeyboardButton(
            text="Agree",
            callback_data=f"client_accept_id:{user.id}:{user.telegram_id}:{user.name_client}"  # Передаем аргумент в callback_data
        )
        button_cancel_client = InlineKeyboardButton(
            text='Cancel',
            callback_data=f'client_cancel_id:{user.id}:{user.telegram_id}:{user.name_client}'
        )
        inline_kb_client = InlineKeyboardMarkup().add(button_accept_client, button_cancel_client)
        return inline_kb_client

    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")