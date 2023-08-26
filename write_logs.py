def write_logs(text):
    with open('errors.txt', 'a+') as file:
        file.write(str(text))