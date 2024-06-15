import re  # Библиотека для работы с регулярными выражениями


# Функция для сохранения строк из пользовательской консоли в список
def save_strings_to_list(strings_list_on_add):
    while True:
        user_input = input("Введите строку (для выхода введите 'exit'): ")  # Запрашиваем строку у пользователя

        if user_input.lower() == 'exit':  # Если пользователь ввел 'exit', выходим из цикла
            break
        # unicode_number = get_unicode_number_first_char(user_input)

        elif user_input.startswith("?-"):  # Если заходим сюда, значит пользователь отправил запрос
            user_input = split_string(user_input, True)
            new_request(user_input, strings_list_on_add)

        elif ":-" in user_input:
            final_string = rule_rewriting(user_input)
            strings_list_on_add.append(final_string)

        else:
            flag_lower = syntax_check(user_input)
            user_input = split_string(user_input, False)
            if flag_lower:
                strings_list_on_add.append(user_input)  # Добавляем введенную строку в список

    return strings_list_on_add  # Возвращаем список сохраненных строк


def syntax_check(input_on_syntax):
    check_flag = True
    if not input_on_syntax.endswith(".") != False:
        print("Ошибка в команде. Команда должна заканчиваться точкой.")
        check_flag = False
    input_on_syntax = split_string(input_on_syntax, False)
    constant_lower = list(map(is_first_lett_lowercase, input_on_syntax))  # Проверка на корректность ввода
    if any(element == False for element in constant_lower):
        print("Ошибка в команде. Если вы хотите написать запрос, то начните строку с символов ?-")
        check_flag = False
    return check_flag


def get_unicode_number_first_char(
        input_string):  # Метод для определения номера первого символа строки в таблице Unicode
    first_char = input_string[0]
    unicode_number = ord(first_char)
    return unicode_number  # Возвращаем номер символа в таблице Unicode


def new_request(input_request, data_list):
    constant_lower = list(map(is_first_lett_lowercase, input_request))
    count_true = constant_lower.count(False)
    var_index_list = []
    const_index_list = []
    summary = []
    for i, var_index in enumerate(constant_lower):
        if constant_lower[i]:
            const_index_list.append([i] + [input_request[i]])
        else:
            # var_index_list.append([i] + [input_request[i]])
            var_index_list.append([input_request[i]])
        summary.append(input_request[i])
    indexes = [var_index_list[0]]
    answers = [[]]
    term_count = len(var_index_list) + len(const_index_list)
    for i, array in enumerate(data_list):
        if term_count == len(array):
            matches = 0
            amount = 0
            for j, element in enumerate(array):
                if element == summary[j]:
                    matches += 1
                elif element != summary[j] and summary[j].isupper():
                    answers[amount].append(element)
                    amount += 1
                    answers.append([])
    for sub_list in answers[:]:
        if not sub_list:
            answers.remove(sub_list)
    print(answers)


def rule_rewriting(user_list):
    cleaned_string = re.sub(r'[^\w\s]', ' ', user_list)
    final_string = re.sub(r'\s+', ' ', cleaned_string)
    final_string = "Запрос: " + final_string
    final_string = final_string[:-1].split(" ")
    return final_string


def is_first_lett_lowercase(arr):  # метод для определения, заглавности первого символа
    if len(arr) > 0:
        first_char = arr[0]
        return first_char.islower()
    else:
        return False


def split_string(input_string, user_command):
    index1 = input_string.find("(")
    index3 = input_string.find(")")
    if user_command:  # Написание новой системы запроса
        first_word = input_string[3:index1].strip()
    else:
        first_word = input_string[:index1].strip()

    words_inside_brackets = input_string[index1 + 1:index3].split(",")
    # Обрабатываем случай, когда в скобках только одно слово
    if len(words_inside_brackets) == 1:
        words_inside_brackets[0] = words_inside_brackets[0].strip()
    # Составляем массив
    result = [first_word] + [word.strip() for word in words_inside_brackets]
    return result


def edit_list(list_to_change):
    # Данный метод необходим для удаления элементов базы знаний
    if check_on_empty(list_to_change):
        return list_to_change
    while True:
        show_list(list_to_change)
        index = input("Введите exit для выхода или индекс элемента для удаления:"
                      "\nвведите all для удаления всей базы знаний: ")
        if index == "exit":
            break
        elif index == "all":
            list_to_change = []
            return list_to_change
        index = int(index)
        if index < 0 or index >= len(list_to_change):
            print("Индекс находится за пределами массива")
        else:
            list_to_change.pop(index)  # Удаляем элемент по указанному индексу
    return list_to_change


def show_list(lists_to_show):
    # Метод для отображения сохранённых строк в базе
    if check_on_empty(lists_to_show):
        return (lists_to_show)
    print("Список сохраненных строк:")
    for i, string in enumerate(lists_to_show):
        output = [string[0]] + ["(" + word + ")" for word in string[1:]]
        # print(len(output))
        if string[0] != "Запрос:":
            print(i, output)
            i += 1
    print("Список сохраненных правил:")
    for i, string in enumerate(lists_to_show):
        output = [string[1]] + [word for word in string[2:]]
        if string[0] == "Запрос:":
            print(i, output)
            i += 1


def add_list(list_to_save):
    # Вызываем функцию и сохраняем список строк
    list_to_save = save_strings_to_list(list_to_save)
    show_list(list_to_save)
    return list_to_save


def check_on_empty(empty_list):  # Метод для проверки того, чтобы пользователь не взаимодействовал с пустым листом
    if len(empty_list) <= 0:
        print("В вашей базе знаний ещё нет информации!"
              "\nФункционал не доступен, пока база знаний пуста.")
        return True
    else:
        return False


def main_menu():
    strings_list = []
    while True:
        command = input("console - работа в консоли \nshow - показать базу знаний "
                        "\nedit - удалить элемент из базы знаний"
                        "\nend - конец работы \nвведите команду: ")
        command = command.lower()
        if command == 'end':
            break
        elif command == 'console':
            strings_list = add_list(strings_list)
        elif command == 'edit':
            strings_list = edit_list(strings_list)
        elif command == 'show':
            show_list(strings_list)
        else:
            print("Неизвестная команда. Повторите ввод")
