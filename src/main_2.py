#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Напишите программу, которая будет генерировать матрицу из случайных целых
# чисел.
# Пользователь может указать число строк и столбцов, а также диапазон целых
# чисел.
# Произведите обработку ошибок ввода пользователя.

from random import randint


def make_matrix(cols, rows, min_val, max_val):
    if min_val > max_val:
        raise ValueError("Minimum value cannot be greater than maximum value")

    if cols < 0 or rows < 0:
        raise ValueError("Number of rows and columns must be greater than zero")

    matrix = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = randint(min_val, max_val)
    return matrix


if __name__ == "__main__":
    while True:
        try:
            cols = int(input("Введите количество столбцов: "))
            rows = int(input("Введите количество строк: "))
            min_val = int(input("Введите минимальное значение: "))
            max_val = int(input("Введите максимальное значение: "))
            print(make_matrix(cols, rows, min_val, max_val))
            break
        except ValueError:
            print("Must be integer")
        except TypeError as e:
            print(e)
