#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import jsonschema
from datetime import datetime


def get_route():
    """
    Запросить данные о маршруте.
    """
    destination = input("Пункт назначения? ")
    number = input("Номер поезда? ")
    time = input("Время отправления?(формат чч:мм) ")

    try:
        datetime.strptime(time, "%H:%M")
    except ValueError:
        print("Неправильный формат времени", file=sys.stderr)
        exit(1)

    return {
        'destination': destination,
        'number': number,
        'time': time
    }


def display_routes(way):
    """
    Отобразить список маршрутов.
    """
    if way:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 4,
            '-' * 20
        )
        print(line)
        print(
            '| {:^30} | {:^4} | {:^20} |'.format(
                "Пункт назначения",
                "№",
                "Время"
            )
        )
        print(line)

        for route in way:
            print(
                '| {:<30} | {:>4} | {:<20} |'.format(
                    route.get('destination', ''),
                    route.get('number', ''),
                    route.get('time', '')
                )
            )
        print(line)

    else:
        print("Маршруты не найдены")


def select_routes(way, period):
    """
    Выбрать маршруты после заданного времени.
    """
    result = []

    for route in way:
        time_route = route.get('time')
        time_route = datetime.strptime(time_route, "%H:%M")
        if period < time_route:
            result.append(route)

    # Возвратить список выбранных маршрутов.
    return result


def save_routes(file_name, way):
    """
    Сохранить все пути в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as f:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(way, f, ensure_ascii=False, indent=4)


def load_routes(file_name):
    """
    Загрузить все пути из файла JSON.
    """

    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string"
                    },
                    "number": {
                        "type": "string"
                    },
                    "time": {
                        "type": "string"
                    }
                },
                "required": [
                    "destination",
                    "number",
                    "time"
                ]
            }
        ]
    }

    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fl:
        data = json.load(fl)

    validator = jsonschema.Draft7Validator(schema)

    try:
        if not validator.validate(data):
            print("Данные успешно загружены")
    except jsonschema.exceptions.ValidationError:
        print("Ошибка загрузки данных", file=sys.stderr)
        exit(1)

    return data


def main():
    """
    Главная функция программы.
    """

    # Список маршрутов.
    routes = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о маршруте.
            route = get_route()

            # Добавить словарь в список.
            routes.append(route)
            # Отсортировать список в случае необходимости.
            if len(routes) > 1:
                routes.sort(key=lambda item: item.get('destination', ''))

        elif command == 'list':
            # Отобразить все маршруты.
            display_routes(routes)

        elif command == 'select':
            time_select = input("Выберите время отправления(формат чч:мм): ")

            try:
                time_select = datetime.strptime(time_select, "%H:%M")
            except ValueError:
                print("Неправильный формат времени", file=sys.stderr)
                exit(1)

            selected = select_routes(routes, time_select)
            # Отобразить выбранные маршруты.
            display_routes(selected)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_routes(file_name, routes)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            routes = load_routes(file_name)

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить маршрут;")
            print("list - вывести список маршрутов;")
            print("select - нати маршруты по времени")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
