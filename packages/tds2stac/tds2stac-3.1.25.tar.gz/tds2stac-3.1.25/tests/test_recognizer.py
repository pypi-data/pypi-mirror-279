# # SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
# #
# # SPDX-License-Identifier: CC0-1.0

from tds2stac import Recognizer


def test_first_case():
    Recognizer(
        "http://localhost:8080/thredds/catalog/catalogs/scenario1/test/catalog.html",
        nested_check=True,
        logger_properties={"logger_handler": "FileHandler"},
    )


def test_second_case():
    Recognizer(
        "http://localhost:8080/thredds/catalog/catalogs/scenario2.html",
        nested_check=True,
        logger_properties={
            "logger_handler": "FileHandler",
            "logger_handler_filename": "test.log",
            "logger_handler_mode": "w",
        },
    )


def test_third_case():
    Recognizer(
        "http://localhost:8080/thredds/catalog/catalogs/scenario3/test/nested/first/catalog.html",
        nested_check=True,
        logger_properties={"logger_handler": "SMTPHandler"},
    )


def test_fourth_case1():
    Recognizer(
        "http://localhost:8080/thredds/catalog/catalogs/scenario4.html",
        logger_properties={"logger_handler": "HTTPHandler"},
    )


def test_fifth_case():
    Recognizer(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html"
    )


def test_sixth_case():
    Recognizer(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html?dataset=a5f5be12-e4de-4977-adb7-a06480f65f48/2020336.nc"
    )


def test_seventh_case():
    Recognizer(
        "http://localhost:8080/thredds/catalog/catalogs/scenario7.html?dataset=2786bf07-8e3b-44d3-82bd-ee27024751ec"
    )


def test_eighth_case():
    Recognizer(
        "http://localhost:8080/thredds/catalog/catalogs/scenario8/test/catalog.html",
        nested_check=True,
    )


def test_ninth_case():
    Recognizer(
        "http://localhost:8080/thredds/catalog/catalogs/scenario9.html",
        nested_check=True,
    )


# def test_first_case():
#     Recognizer(
#         "http://localhost:8080/thredds/catalog/catalogs/scenario1/test/catalog.html",
#         nested_check=True,
#         logger_properties={"logger_handler": "FileHandler"},
#     )


# def test_second_case():
#     Recognizer(
#         "https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/sensor_catalog_ext.html",
#         nested_check=True,
#         logger_properties={
#             "logger_handler": "FileHandler",
#             "logger_handler_filename": "test.log",
#             "logger_handler_mode": "w",
#         },
#     )


# def test_third_case():
#     Recognizer(
#         "https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/catalog.html",
#         nested_check=True,
#         logger_properties={"logger_handler": "SMTPHandler"},
#     )


# def test_fourth_case1():
#     Recognizer(
#         "https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/bio_geo_chem_catalog_ext.xml",
#         logger_properties={"logger_handler": "HTTPHandler"},
#     )


# def test_fifth_case():
#     Recognizer(
#         "https://thredds.imk-ifu.kit.edu/thredds/catalog/climate/raster/global/chelsa/v1.2/catalog.html"
#     )


# def test_sixth_case():
#     Recognizer(
#         "https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/era5/sfc/single/daily/catalog.html?dataset=era5_sfc_0.25_single/daily/ERA5_daily_sp_1981.nc"
#     )


# def test_seventh_case():
#     Recognizer(
#         "https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/swabian_moses_2021.html?dataset=swabian_moses_aggregation"
#     )


# def test_eighth_case():
#     Recognizer(
#         "https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/transfer.html",
#         nested_check=True,
#     )


# def test_ninth_case():
#     Recognizer(
#         "https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/hydrogfd/v3.0/catalog.html",
#         nested_check=True,
#     )


# def test_case_finder():
#     Recognizer(
#         "https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/reg_clim_sys_catalog_ext.html",
#         nested_check=True,
#     )
