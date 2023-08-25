from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


city_nz_y = KeyboardButton(text='Нью-Йорк')
city_l_a = KeyboardButton(text='Лос-Анджелес')
city_may = KeyboardButton(text='Майами')
another = KeyboardButton(text='Другое')
cancela = KeyboardButton(text='Отмена')
default_cities = ReplyKeyboardMarkup(resize_keyboard=True).add(city_may, city_l_a, city_nz_y, another, cancela)

h_curr_usd_g = KeyboardButton(text='USD Наличными')
h_curr_usd_ng = KeyboardButton(text='USD Безналичными')
h_curr_usdt_ng = KeyboardButton(text='USDT')
anotherr = KeyboardButton(text='Другое')
cancell = KeyboardButton(text='Отмена')
h_curr_all = ReplyKeyboardMarkup(resize_keyboard=True).add(h_curr_usd_ng, h_curr_usd_g, h_curr_usdt_ng, anotherr, cancell)

h_curr_a_btc = KeyboardButton(text='BTC')
h_curr_a_rub = KeyboardButton(text='RUB')
h_curr_a_eur = KeyboardButton(text='EUR')
h_curr_a_anoth = KeyboardButton(text='Другое')
h_curr_a = ReplyKeyboardMarkup(resize_keyboard=True).add(h_curr_a_btc, h_curr_a_rub, h_curr_a_eur, h_curr_a_anoth)

bts = KeyboardButton(text='BTS')
rub = KeyboardButton(text='RUB')
eur = KeyboardButton(text='EUR')
anotherrr = KeyboardButton(text='Еще другое')
another_rm = ReplyKeyboardMarkup(resize_keyboard=True).add(anotherrr, eur, rub, bts)

cancel = KeyboardButton(text='Отмена')
main_but = ReplyKeyboardMarkup(resize_keyboard=True).add(cancel)

start = KeyboardButton(text='/start')
start_key = ReplyKeyboardMarkup(resize_keyboard=True).add(start)

rachnunek = KeyboardButton(text='Оплата на счет за услуги/недвижимость')
gotowka = KeyboardButton(text='Наличные')
beznaja = KeyboardButton(text='Безналичные')
another_view = KeyboardButton(text='Другое')
cancel_view = KeyboardButton(text='Отмена')
view_money = ReplyKeyboardMarkup(resize_keyboard=True).add(gotowka,beznaja,another_view,rachnunek,cancel_view)

non_cash_b = KeyboardButton(text="Юридичесское лицо")
non_cash_f = KeyboardButton(text="Физичесское лицо")
non_cash = ReplyKeyboardMarkup(resize_keyboard=True).add(non_cash_f, non_cash_b)

how_curr_dir = KeyboardButton(text='AED')
how_curr_usd = KeyboardButton(text='USD')
how_curr_tange = KeyboardButton(text='KZT')
another_how_curr = KeyboardButton(text='Другое')
cancel_how_curr = KeyboardButton(text='Отмена')
how_surr = ReplyKeyboardMarkup(resize_keyboard=True).add(how_curr_dir,how_curr_usd,how_curr_tange,another_how_curr, cancel_how_curr)

how_curr_eur = KeyboardButton(text='EUR')
how_curr_gbp = KeyboardButton(text='GBP')
how_curr_yen = KeyboardButton(text='YEN')
how_curr_chf = KeyboardButton(text='CHF')
how_curr_rub = KeyboardButton(text='RUB')
how_curr_add = ReplyKeyboardMarkup(resize_keyboard=True).add(how_curr_rub, how_curr_chf, how_curr_yen, how_curr_gbp, how_curr_eur)

to_city_dubai = KeyboardButton(text='Дубаи')
to_city_mock = KeyboardButton(text='Москва')
to_city_alma = KeyboardButton(text='Алматы')
to_city_cancel = KeyboardButton(text='Отмена')
to_city_anothar = KeyboardButton(text='Другое')
to_city = ReplyKeyboardMarkup(resize_keyboard=True).add(to_city_dubai,to_city_mock,to_city_alma,to_city_cancel,to_city_anothar)