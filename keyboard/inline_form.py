from aiogram import types
import serializator
from config import n

buttons_per_page = 3


def send_paginated_buttons(page, number_cell=None, button_list_domestic=None, is_city=None):
    button_list = []
    if is_city is not None:
        button_list = is_city
        n['key_city'] = is_city
    else:
        button_lists = serializator.parse_buttons(place=number_cell, buttons=button_list_domestic)
        button_list = button_lists[1]
    start_idx = (page - 1) * buttons_per_page
    end_idx = start_idx + buttons_per_page
    buttons = button_list[start_idx:end_idx]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for button_text in buttons:
        button = types.InlineKeyboardButton(text=button_text, callback_data=f'button:{button_text}')
        keyboard.insert(button)

    free_button = types.InlineKeyboardButton(text="Your option", callback_data=f'add_option:null:{number_cell}')
    keyboard.insert(free_button)

    if start_idx > 0:
        prev_page_button = types.InlineKeyboardButton(text="←", callback_data=f'prev_page:{page - 1}:{number_cell}')
        keyboard.insert(prev_page_button)

    elif start_idx in list(range(len(button_list))):
        prev_page_button = types.InlineKeyboardButton(text="←", callback_data=f'prev_page:{page - 1}:{number_cell}')
        next_page_button = types.InlineKeyboardButton(text="→", callback_data=f'next_page:{page + 1}:{number_cell}')
        keyboard.row(prev_page_button, next_page_button)

    elif end_idx < len(button_list):
        next_page_button = types.InlineKeyboardButton(text="→", callback_data=f'next_page:{page+1}:{number_cell}')
        keyboard.insert(next_page_button)

    return keyboard
