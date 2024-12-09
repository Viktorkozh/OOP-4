#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего варианта лабораторной работы 2.17 добавьте возможность хранения
# файла данных в домашнем каталоге пользователя. Для выполнения операций с
# файлами необходимо использовать модуль pathlib.

# Выполнить индивидуальное задание 1 лабораторной работы 2.19,
# добавив возможность работы с исключениями и логгирование.

from pathlib import Path
import argparse
import json
import os
from datetime import datetime
import jsonschema
import logging

logging.basicConfig(level=logging.DEBUG)

person_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "surname": {"type": "string"},
        "date_of_birth": {"type": "string", "format": "date"},
        "zodiac_sign": {"type": "string"},
    },
    "required": ["name", "surname", "date_of_birth", "zodiac_sign"],
}


def validate_person(person_data, schema):
    try:
        jsonschema.validate(person_data, schema)
        datetime.strptime(person_data["date_of_birth"], "%d.%m.%Y")
        return True
    except jsonschema.exceptions.ValidationError as e:
        logging.error(f"Данные человека не соответствуют схеме: {e}")
        return False
    except ValueError as e:
        logging.error(f"Ошибка при разборе даты: {e}")
        return False


def add_person(people, name, surname, date_of_birth, zodiac_sign):
    """
    Добавление нового человека в список.
    Список сортируется по знаку зодиака после добавления нового элемента.
    """
    date_of_birth = datetime.strptime(date_of_birth, "%d.%m.%Y")

    person = {
        "name": name,
        "surname": surname,
        "date_of_birth": date_of_birth,
        "zodiac_sign": zodiac_sign,
    }

    people.append(person)
    people.sort(key=lambda item: item.get("zodiac_sign", ""))
    return people


def list_people(people):
    """
    Вывод таблицы людей.
    """
    line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
        "-" * 4, "-" * 20, "-" * 20, "-" * 15, "-" * 13
    )
    print(line)
    print(
        "| {:^4} | {:^20} | {:^20} | {:^15} | {:^12} |".format(
            "№", "Имя", "Фамилия", "Знак Зодиака", "Дата рождения"
        )
    )
    print(line)

    for idx, person in enumerate(people, 1):
        birth_date_str = person.get("date_of_birth").strftime("%d.%m.%Y")
        print(
            "| {:^4} | {:<20} | {:<20} | {:<15} | {:<13} |".format(
                idx,
                person.get("name", ""),
                person.get("surname", ""),
                person.get("zodiac_sign", ""),
                birth_date_str,
            )
        )

    print(line)


def select_people(people, month):
    """
    Вывести список людей, родившихся в заданном месяце.
    """
    count = 0
    for person in people:
        if person.get("date_of_birth").month == month:
            count += 1
            print(
                "{:>4}: {} {}".format(
                    count, person.get("name", ""), person.get("surname", "")
                )
            )

    if count == 0:
        print("Люди, родившиеся в указанном месяце, не найдены.")


def save_people(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    staff_formatted = [
        {**person, "date_of_birth": person.get("date_of_birth").strftime("%d.%m.%Y")}
        for person in staff
    ]
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        json.dump(staff_formatted, fout, ensure_ascii=False, indent=4)


def load_people(file_name):
    """
    Загрузить всех людей из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        staff_loaded = json.load(fin)
        result_people = []
        cnt = 0
        for person in staff_loaded:
            cnt += 1
            if validate_person(person, person_schema):
                try:
                    person["date_of_birth"] = datetime.strptime(
                        person["date_of_birth"], "%d.%m.%Y"
                    )
                    result_people.append(person)
                except ValueError:
                    logging.error(
                        "Ошибка при разборе даты в записи, пропуск записи" f"{cnt}."
                    )
            else:
                logging.error("Неверные данные человека, пропуск записи.")
        return result_people


def test():
    people = [
        {
            "name": "John",
            "surname": "Doe",
            "date_of_birth": datetime.strptime("01.01.1990", "%d.%m.%Y"),
            "zodiac_sign": "Capricorn",
        }
    ]
    return validate_person(people[0], person_schema)


def main():
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument("filename", action="store", help="The data file name")
    # Создание основного парсера.
    parser = argparse.ArgumentParser(description="Управление списком людей")
    subparsers = parser.add_subparsers(dest="command")

    # Создание парсера для тестирования.
    _ = subparsers.add_parser("test", help="Тестирование программы")

    # Создание парсера для добавления человека.
    parser_add = subparsers.add_parser(
        "add", parents=[file_parser], help="Добавить человека"
    )
    parser_add.add_argument("-n", "--name", help="Имя человека")
    parser_add.add_argument("-s", "--surname", help="Фамилия человека")
    parser_add.add_argument(
        "-d", "--date_of_birth", help="Дата рождения (формат ДД.ММ.ГГГГ)"
    )
    parser_add.add_argument("-z", "--zodiac_sign", help="Знак зодиака")

    # Создание парсера для вывода списка людей.
    _ = subparsers.add_parser(
        "list", parents=[file_parser], help="Вывести список людей"
    )

    # Создание парсера для выбора человека по месяцу рождения.
    parser_select = subparsers.add_parser(
        "select", parents=[file_parser], help="Выбрать людей по месяцу рождения"
    )
    parser_select.add_argument("-m", "--month", type=int, help="Месяц рождения")

    # Разбираем аргументы командной строки.
    args = parser.parse_args()

    if args.command == "test":
        test()

    is_dirty = False

    home_directory = Path.home()
    data_directory = home_directory / "data"
    # Создаем каталог, если он не существует.
    data_directory.mkdir(exist_ok=True)
    try:
        filename = data_directory / args.filename
    except Exception:
        logging.error("Отсутствуют один или нестолько обязательных аргументов.")
        exit(1)

    if os.path.exists(filename):
        try:
            people = load_people(filename)
        except Exception:
            logging.error("Ошибка при загрузке данных из файла.")
            exit(1)
    else:
        people = []

    # Определяем, какую команду нужно выполнить.
    if args.command == "add":
        try:
            people = add_person(
                people, args.name, args.surname, args.date_of_birth, args.zodiac_sign
            )
            is_dirty = True
        except Exception:
            logging.error("Отсутствуют один или нестолько обязательных аргументов.")

    elif args.command == "list":
        list_people(people)

    elif args.command == "select":
        select_people(people, args.month)

    if is_dirty:
        save_people(filename, people)


if __name__ == "__main__":
    main()
