from config import w_another, w_cancel, bot
from keyboard import start_key


async def check_text(message, current_state, next_state, reply_mark, state, text_another, success_text, key, add=None):
    if message.text == str(w_another):
        if add != None:
            await bot.send_message(message.chat.id, f"Напишите валюту либо выберите из списка:", reply_markup=add)
        else:
            await bot.send_message(message.chat.id, f"{text_another}")
        await current_state.set()
    elif message.text == str(w_cancel):
        await state.finish()
        await bot.send_message(message.chat.id, "Отменено!\nЧто бы начать заново /start", reply_markup=start_key)
    else:
        async with state.proxy() as data:
            data[f'{key}'] = message.text

        await bot.send_message(message.chat.id, f"{success_text}", reply_markup=reply_mark)
        await next_state.set()