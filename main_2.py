#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Напишите программу, которая будет генерировать матрицу из случайных целых чисел.
# Пользователь может указать число строк и столбцов, а также диапазон целых чисел.
# Произведите обработку ошибок ввода пользователя.

from random import randint


def make_matrix(cols, rows, min, max):
    matrix = [[0]*cols for i in range(rows)]
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = randint(min, max)
    return matrix


if __name__ == "__main__":
    while True:
        try:
            cols = int(input("Введите количество столбцов: "))
            rows = int(input("Введите количество строк: "))
            min = int(input("Введите минимальное значение: "))
            max = int(input("Введите максимальное значение: "))
            if min > max:
                raise TypeError("Минимальное значение больше максимального")
            print(make_matrix(cols, rows, min, max))
            break
        except ValueError as e:
            print("Must be integer")
        except TypeError as e:
            print(e)
