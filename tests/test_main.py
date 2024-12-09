#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from main import sum_two_numbers


def test_sum_two_numbers_valid_inputs():
    assert sum_two_numbers("3", "5") == 8
    assert sum_two_numbers("10", "20") == 30
    assert sum_two_numbers("-1", "1") == 0
    assert sum_two_numbers("0", "0") == 0


def test_sum_two_numbers_invalid_inputs():
    assert sum_two_numbers("abc", "5") == "abc5"
    assert sum_two_numbers("3", "xyz") == "3xyz"
    assert sum_two_numbers("abc", "xyz") == "abcxyz"
    assert sum_two_numbers("3.5", "2") == "3.52"
