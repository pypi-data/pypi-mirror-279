# # SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
# #
# # SPDX-License-Identifier: CC0-1.0

# import sys

# from tds2stac.main_app import Nested_Collections

# sys.path.append("../")
from tds2stac import NestedCollectionInspector


def test_first_case_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario1/test/catalog.html",
    )


def test_first_case_gt_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario1/test/catalog.html",
        nested_number=1,
    )


def test_second_case_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario2.html",
        nested_number=0,
    )


def test_second_case_gt_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario2.html",
        nested_number=1,
    )


def test_third_case_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario3/test/nested/first/catalog.html",
        nested_number=0,
    )


def test_third_case_gt_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario3/test/nested/first/catalog.html",
        nested_number=1,
    )


def test_eighth_case_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario8.html",
        nested_number=0,
    )


def test_eighth_case_gt_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario8.html",
        nested_number=1,
    )


def test_ninth_case_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario9.html",
        nested_number=0,
    )


def test_ninth_case_gt_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/scenario9.html",
        nested_number=1,
    )


def test_random_case_0():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/main.html",
        nested_number=0,
    )


def test_random_case_1():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/main.html",
        nested_number=1,
    )


def test_random_case_2():
    NestedCollectionInspector(
        "http://localhost:8080/thredds/catalog/catalogs/main.html",
        nested_number=2,
    )
