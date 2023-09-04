import loguru
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_inline_join_client(telegram_id):
    try:
        button_accept_operator = InlineKeyboardButton(
            text="Accept",
            callback_data=f"join_accept:{telegram_id}"  # Передаем аргумент в callback_data
        )
        button_cancel_operator = InlineKeyboardButton(
            text='Cancel',
            callback_data=f'join_cancel:{telegram_id}'
        )
        inline_kb = InlineKeyboardMarkup().add(button_accept_operator, button_cancel_operator)
        return inline_kb

    except Exception as error:
        loguru.logger.critical(error)


def get_inline_join_operator(telegram_id):
    try:
        button_accept_operator = InlineKeyboardButton(
            text="Accept",
            callback_data=f"join_accept_operator:{telegram_id}"  # Передаем аргумент в callback_data
        )
        button_cancel_operator = InlineKeyboardButton(
            text='Cancel',
            callback_data=f'join_cancel_operator:{telegram_id}'
        )
        inline_kb = InlineKeyboardMarkup().add(button_accept_operator, button_cancel_operator)
        return inline_kb

    except Exception as error:
        loguru.logger.critical(error)

