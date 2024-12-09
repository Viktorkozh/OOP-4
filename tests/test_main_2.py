#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from main_2 import make_matrix


def test_make_matrix_valid_inputs():
    matrix = make_matrix(3, 2, 1, 5)
    assert len(matrix) == 2
    assert all(len(row) == 3 for row in matrix)
    assert all(1 <= cell <= 5 for row in matrix for cell in row)


def test_make_matrix_invalid_min_max():
    with pytest.raises(
        ValueError, match="Minimum value cannot be greater than maximum value"
    ):
        make_matrix(3, 2, 5, 1)


def test_make_matrix_zero_dimensions():
    matrix = make_matrix(0, 0, 1, 5)
    assert matrix == []


def test_make_matrix_negative_dimensions():
    with pytest.raises(ValueError):
        make_matrix(-1, 2, 1, 5)
    with pytest.raises(ValueError):
        make_matrix(2, -1, 1, 5)
