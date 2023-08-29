def ser(user):
    return f"id: {user.id}\nUsername: {user.name_client}\nTelegram id: {user.telegram_id}\nSending from: {user.city_from}\nSending: {user.curr_set}\nAmount: {user.total}\nSending to: {user.city_to}\nReceving: {user.curr_get}"

def ser_admin(user):
    return f"Username: {user.name_client}\nTelegram id: {user.telegram_id}\nSending from: {user.city_from}\nSending: {user.curr_set}\nAmount: {user.total}\nSending to: {user.city_to}\nReceving: {user.curr_get}"

def view_json_output(data):
    return f"Sending from: {data['city_from']}\nWhat are you sending: {data['curr_set']}\nAmount: {data['total']}\nSending to: {data['city_to']}\nWhat are you receiving: {data['curr_get']}"


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

def get_operators_from_sheet(values):
    id_operators_values = []
    for entry in values:
        if len(entry) >= 2 and entry[0] == 'ID OPERATORS':
            id_operators_values.extend(entry[1:])

    return id_operators_values