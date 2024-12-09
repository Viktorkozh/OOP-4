#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from typing import Any
from main_3 import (
    add_person,
    list_people,
    select_people,
    save_people,
    load_people,
    validate_person,
    person_schema,
)
from datetime import datetime
import json


def test_validate_person_valid():
    person = {
        "name": "Виктор",
        "surname": "Кожуховский",
        "date_of_birth": "01.01.1990",
        "zodiac_sign": "Знак",
    }
    assert validate_person(person, person_schema) is True


def test_validate_person_invalid():
    person = {
        "name": "Виктор",
        "surname": "Кожуховский",
        "date_of_birth": "878974",
        "zodiac_sign": "Знак",
    }
    assert validate_person(person, person_schema) is False


def test_add_person():
    people = []
    people = add_person(people, "Виктор", "Кожуховский", "06.03.2004", "Знак")
    assert len(people) == 1
    assert people[0]["name"] == "Виктор"
    assert people[0]["surname"] == "Кожуховский"
    assert people[0]["zodiac_sign"] == "Знак"
    assert people[0]["date_of_birth"] == datetime.strptime("06.03.2004", "%d.%m.%Y")


def test_list_people(capsys: pytest.CaptureFixture[Any]):
    people = [
        {
            "name": "Виктор",
            "surname": "Кожуховский",
            "date_of_birth": datetime.strptime("06.03.2004", "%d.%m.%Y"),
            "zodiac_sign": "Знак",
        },
        {
            "name": "Имя",
            "surname": "Фамилия",
            "date_of_birth": datetime.strptime("15.05.1992", "%d.%m.%Y"),
            "zodiac_sign": "Taurus",
        },
    ]
    list_people(people)
    captured = capsys.readouterr()
    assert "Виктор" in captured.out.strip()
    assert "Имя" in captured.out.strip()


def test_select_people(capsys: pytest.CaptureFixture[Any]):
    people = [
        {
            "name": "Виктор",
            "surname": "Кожуховский",
            "date_of_birth": datetime.strptime("06.03.2004", "%d.%m.%Y"),
            "zodiac_sign": "Знак",
        },
        {
            "name": "Имя",
            "surname": "Фамилия",
            "date_of_birth": datetime.strptime("15.05.1992", "%d.%m.%Y"),
            "zodiac_sign": "Taurus",
        },
    ]
    select_people(people, 3)
    captured = capsys.readouterr()
    assert len(captured) == 2
    assert "Виктор Кожуховский" in captured.out.strip()


def test_save_load_people(tmp_path):
    people = [
        {
            "name": "Виктор",
            "surname": "Кожуховский",
            "date_of_birth": datetime.strptime("06.03.2004", "%d.%m.%Y"),
            "zodiac_sign": "Знак",
        }
    ]
    test_file = tmp_path / "test_people.json"
    save_people(test_file, people)

    loaded_people = load_people(test_file)
    assert len(loaded_people) == 1
    assert loaded_people[0]["name"] == "Виктор"
    assert loaded_people[0]["surname"] == "Кожуховский"


def test_load_people_invalid_data(tmp_path):
    invalid_data = [
        {
            "name": "Виктор",
            "surname": "Кожуховский",
            "date_of_birth": "not-a-date",
            "zodiac_sign": "Знак",
        }
    ]
    test_file = tmp_path / "invalid_people.json"
    with open(test_file, "w", encoding="utf-8") as fout:
        json.dump(invalid_data, fout, ensure_ascii=False, indent=4)

    loaded_people = load_people(test_file)
    assert len(loaded_people) == 0  # Should skip invalid entries
