def ser(user):
    try:
        return f"id: {user.id}\nUsername: {user.name_client}\nTelegram id: {user.telegram_id}\nSending from: {user.city_from}\nSending: {user.curr_set}\nAmount: {user.total}\nSending to: {user.city_to}\nReceving: {user.curr_get}"

    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")


def ser_admin(user):
    try:
        return f"Username: {user.name_client}\nTelegram id: {user.telegram_id}\nSending from: {user.city_from}\nSending: {user.curr_set}\nAmount: {user.total}\nSending to: {user.city_to}\nReceving: {user.curr_get}"

    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")


def view_json_output(data):
    try:
        return f"Sending from: {data['city_from']}\nWhat are you sending: {data['curr_set']}\nAmount: {data['total']}\nSending to: {data['city_to']}\nWhat are you receiving: {data['curr_get']}"

    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")


def parse_buttons(place, buttons):
    try:
        first_element = buttons[place]
        split_elements = [element.split(', ') for element in first_element]
        return split_elements

    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")


def search_city(data, selected_city):
    try:
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
            return []

    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")


def get_operators_from_sheet(values):
    try:
        id_operators_values = []
        for entry in values:
            if len(entry) >= 2 and entry[0] == 'ID OPERATORS':
                id_operators_values.extend(entry[1:])

        return id_operators_values

    except Exception as error:
        from logconfig import setup_logging
        logger = setup_logging()
        logger.error(f"{error}")