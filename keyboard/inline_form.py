from aiogram import types
import serializator

buttons_per_page = 3


def send_paginated_buttons(page, number_cell, button_list_domestic=None):
    button_lists = serializator.parse_buttons(place=number_cell, buttons=button_list_domestic)
    button_list = button_lists[1]
    start_idx = (page - 1) * buttons_per_page
    end_idx = start_idx + buttons_per_page
    buttons = button_list[start_idx:end_idx]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for button_text in buttons:
        button = types.InlineKeyboardButton(text=button_text, callback_data=f'button:{button_text}')
        keyboard.insert(button)

    if end_idx < len(button_list):
        next_page_button = types.InlineKeyboardButton(text="Another", callback_data=f'next_page:{page+1}:{number_cell}')
        keyboard.insert(next_page_button)

    return keyboard
