def ser(user):
    return f"id: {user.id}\nИмя: {user.name_client}\ntelegram id: {user.telegram_id}\nС какого города: {user.city_from}\nВ какой валюте: {user.curr_set}\nСумма: {user.total}\nВ какой город: {user.city_to}\nВ какой валюте получить: {user.curr_get}\nВ каком виде: {user.view_money}"


def parse_buttons(place, buttons):
    first_element = buttons[place]
    split_elements = [element.split(', ') for element in first_element]
    return split_elements

