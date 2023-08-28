def ser(user):
    return f"id: {user.id}\nИмя: {user.name_client}\ntelegram id: {user.telegram_id}\nС какого города: {user.city_from}\nВ какой валюте: {user.curr_set}\nСумма: {user.total}\nВ какой город: {user.city_to}\nВ какой валюте получить: {user.curr_get}\nВ каком виде: {user.view_money}"


def parse_buttons(place, buttons):
    first_element = buttons[place]
    split_elements = [element.split(', ') for element in first_element]
    return split_elements

def search_city(data, selected_city):
    dependencies_index = None
    for index, row in enumerate(data):
        if row[0] == 'Зависимости':
            dependencies_index = index
            break

    if dependencies_index is not None:
        # Розділимо рядок "Зависимості" на список міст і їх залежності
        dependencies = data[dependencies_index][1:]
        dependencies_dict = {}
        for dependency in dependencies:
            city, dependencies_info = dependency.split(': ')
            dependencies_dict[city] = dependencies_info.split(', ')

        # Ваш аргумент, наприклад "Майами"
        # Отримаємо залежності для вибраного міста
        if selected_city in dependencies_dict:
            selected_dependencies = dependencies_dict[selected_city]
            return selected_dependencies
        else:
            return []
    else:
        print("Рядок 'Зависимости' не знайдено")