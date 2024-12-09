#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Напишите программу, которая запрашивает ввод двух значений.
# Если хотя бы одно из них не является числом,
# то должна выполняться конкатенация, т. е. соединение строк.
# В остальных случаях введенные числа суммируются.


def sum_two_numbers(val, val2):
    try:
        val = int(val)
        val2 = int(val2)
        return val + val2
    except ValueError:
        return f"{val}{val2}"


if __name__ == "__main__":
    val = input("input first number: ")
    val2 = input("input second number: ")
    result = sum_two_numbers(val, val2)
    print("Сумма: ", result)
