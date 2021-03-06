#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
test_trouve_inclusions.py : //
"""


import config
import pytest

from tycat import read_instance
from utils import get_files_matching_ext
from main import trouve_inclusions, trouve_inclusions_sorted
from segments_intersections import trouve_inclusions_segments
from line_intersections import trouve_inclusions_lines
from point_in_polygon_general import trouve_inclusions_general
from point_in_polygon_general_bis import trouve_inclusions_bis


# TROUVE_INCLUSIONS_FUNCTIONS = (trouve_inclusions)
POLY_FILES = get_files_matching_ext(
    ".poly", exceptions=[config.TESTS_PATH + f"upper_and_left_duplication_{i}.poly" for i in [256, 512]]
)
# [config.TESTS_PATH + "generated.poly"] + [config.TESTS_PATH + f"generated_from_examples_{i}.poly" for i in [2, 4, 8, 16, 64, 128, 256]]
TESTS_INCLUSIONS = [
    (config.TESTS_PATH + "10x10.poly", [-1, 0]),
    (config.TESTS_PATH + "e2.poly", [1, -1, 0, 0]),
    (config.TESTS_PATH + "e20.poly", [-1, 0, 1, 1]),
    (config.TESTS_PATH + "e21.poly", [-1, 0, 1, 2]),
    (config.TESTS_PATH + "e3.poly", [-1, 0, 1, 1, -1, 4, 5, 5]),
    (
        config.TESTS_PATH + "upper_and_left_duplication_2.poly",
        [1, -1, 0, 0, 5, -1, 4, 4, 9, -1, 8, 8],
    ),
]
TROUVE_INCLUSIONS_FUNCTIONS = [
    trouve_inclusions_sorted,
    #trouve_inclusions_segments,
    trouve_inclusions_general,
    #trouve_inclusions,
    trouve_inclusions_bis
]
TROUVE_INCLUSIONS_FUNCTIONS_BAD = [
    trouve_inclusions_lines
]


@pytest.mark.parametrize("file", POLY_FILES)
def test_compare_functions(file, functions=TROUVE_INCLUSIONS_FUNCTIONS):
    polygones = read_instance(file)
    results = [function(polygones) for function in functions]
    for indice, (res1, res2) in enumerate(zip(results, results[1:])):
        print("Numéro de la comparaison : ", indice)
        assert(res1 == res2)

@pytest.mark.parametrize("file, expected", TESTS_INCLUSIONS)
def test_inclusions(expected, file, function=trouve_inclusions_sorted):
    polygones = read_instance(file)
    assert function(polygones) == expected
