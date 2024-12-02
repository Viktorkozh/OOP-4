#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
# Замените 'your_module' на имя вашего файла без .py
from example_1 import Staff, Worker, IllegalYearError, UnknownCommandError


def test_add_worker():
    staff = Staff()
    staff.add("John Doe", "Developer", 2020)
    assert len(staff.workers) == 1
    assert staff.workers[0] == Worker(
        name="John Doe", post="Developer", year=2020)


def test_add_worker_illegal_year():
    staff = Staff()
    with pytest.raises(IllegalYearError):
        staff.add("Jane Doe", "Manager", 2025)  # Год больше текущего

    with pytest.raises(IllegalYearError):
        staff.add("Jane Doe", "Manager", -1)  # Неверный год


def test_select_workers():
    staff = Staff()
    staff.add("Alice Smith", "Designer", 2018)
    staff.add("Bob Johnson", "Developer", 2020)
    staff.add("Charlie Brown", "Manager", 2015)

    selected = staff.select(5)  # Работники со стажем более 5 лет
    assert len(selected) == 2  # Alice и Charlie должны быть выбраны
    assert selected[0].name == "Alice Smith"
    assert selected[1].name == "Charlie Brown"


def test_select_no_workers():
    staff = Staff()
    staff.add("Alice Smith", "Designer", 2020)
    selected = staff.select(5)  # Работников со стажем более 5 лет нет
    assert len(selected) == 0


def test_str_representation():
    staff = Staff()
    staff.add("Alice Smith", "Designer", 2018)
    staff.add("Bob Johnson", "Developer", 2020)
    expected_output = (
        "+----+------------------------------+--------------------+--------+\n"
        "| №  | Ф.И.О.                       | Должность          | Год    |\n"
        "+----+------------------------------+--------------------+--------+\n"
        "| 1  | Alice Smith                 | Designer           | 2018   |\n"
        "| 2  | Bob Johnson                 | Developer          | 2020   |\n"
        "+----+------------------------------+--------------------+--------+\n"
    )
    assert str(staff) == expected_output


def test_unknown_command_error():
    with pytest.raises(UnknownCommandError):
        raise UnknownCommandError("invalid_command")
