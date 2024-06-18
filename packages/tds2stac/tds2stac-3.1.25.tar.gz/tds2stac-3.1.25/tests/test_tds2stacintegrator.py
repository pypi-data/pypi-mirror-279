# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
from tds2stac import TDS2STACIntegrator


# nested depth = 0
def test_tds2stacintegrator_nested_depth_zero_all_possible_extensions():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=0,
        extension_properties={
            "item_extensions": [
                "common_metadata",
                "item_datacube_extension",
                (
                    "scientific_extension",
                    "item",
                    "./custom_based_on_defined_extension_pystac.py",
                ),
                (
                    "contact_extension",
                    "item",
                    "./custom_based_on_none_defined_extension_pystac.py",
                ),
            ],
        },
    )


def test_tds2stacintegrator_extra_metadata():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario3/test/nested/first/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=0,
        extra_metadata={"extra_metadata": True},
    )


def test_tds2stacintegrator_nested_depth_zero_with_webservice():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        datetime_filter=["2010-02-18T00:00:00Z", "2010-02-18T00:00:00Z"],
        depth_number=0,
        webservice_properties={
            "web_service_config_file": "./tag_example.json",
        },
    )


def test_tds2stacintegrator_nested_depth_zero_without_webservice():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=0,
    )


def test_tds2stacintegrator_nested_depth_zero_with_asset():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html?dataset=a5f5be12-e4de-4977-adb7-a06480f65f48/2020336.nc",
        stac_dir="stac/",
        limited_number=2,
        depth_number=0,
        webservice_properties={
            "web_service_config_file": "./tag_example.json",
        },
        extension_properties={
            "item_extensions": [
                "common_metadata",
                "item_datacube_extension",
                (
                    "scientific_extension",
                    "item",
                    "./custom_based_on_defined_extension_pystac.py",
                ),
                (
                    "contact_extension",
                    "item",
                    "./nn/custom_based_on_none_defined_extension_pystac.py",
                ),
            ],
        },
        asset_properties={
            "item_thumbnail": True,
            "item_getminmax_thumbnail": True,
            "explore_data": True,
            "verify_explore_data": True,
            "jupyter_notebook": True,
            "collection_thumbnail": "link",
            "collection_overview": "wms",
            "collection_thumbnail_link": "https://images.fineartamerica.com/images-medium-large-5/global-precipitation-william-putmannasa-goddard-space-flight-center.jpg",
            "assets_list_allowed": ["wms", "wcs", "wfs"],
            "assets_list_avoided": ["http"],
        },
    )


# nested depth gt zero
def test_tds2stacintegrator_nested_depth_gt_zero_all_possible_extensions():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=1,
        extension_properties={
            "item_extensions": [
                "common_metadata",
                "item_datacube_extension",
                (
                    "scientific_extension",
                    "item",
                    "./custom_based_on_defined_extension_pystac.py",
                ),
                (
                    "contact_extension",
                    "item",
                    "./custom_based_on_none_defined_extension_pystac.py",
                ),
            ],
        },
    )


def test_tds2stacintegrator_nested_depth_gt_zero_with_webservice():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=1,
        webservice_properties={
            "web_service_config_file": "./tag_example.json",
        },
    )


def test_tds2stacintegrator_nested_depth_gt_zero_without_webservice():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=1,
    )


def test_tds2stacintegrator_nested_depth_gt_zero_with_asset():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=1,
        depth_number=1,
        webservice_properties={
            "web_service_config_file": "./tag_example.json",
        },
        extension_properties={
            "item_extensions": [
                "common_metadata",
                "item_datacube_extension",
                (
                    "scientific_extension",
                    "item",
                    "./custom_based_on_defined_extension_pystac.py",
                ),
                (
                    "contact_extension",
                    "item",
                    "./nn/custom_based_on_none_defined_extension_pystac.py",
                ),
            ],
        },
        asset_properties={
            "item_thumbnail": True,
            "item_overview": True,
            "item_getminmax_thumbnail": True,
            "explore_data": True,
            "verify_explore_data": True,
            "jupyter_notebook": True,
            "collection_thumbnail": "link",
            "collection_overview": "wms",
            "collection_thumbnail_link": "https://images.fineartamerica.com/images-medium-large-5/global-precipitation-william-putmannasa-goddard-space-flight-center.jpg",
            "assets_list_allowed": ["wms", "wcs", "wfs"],
            "assets_list_avoided": ["http"],
        },
    )


# Another case
def test_tds2stacintegrator_nested_depth_gt_zero_all_possible_extensions1():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario3/test/nested/first/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=1,
        extension_properties={
            "item_extensions": [
                "common_metadata",
                "item_datacube_extension",
                (
                    "scientific_extension",
                    "item",
                    "./custom_based_on_defined_extension_pystac.py",
                ),
                (
                    "contact_extension",
                    "item",
                    "./custom_based_on_none_defined_extension_pystac.py",
                ),
            ],
        },
    )


def test_tds2stacintegrator_nested_depth_gt_zero_with_webservice1():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario3/test/nested/first/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=1,
        webservice_properties={
            "web_service_config_file": "./tag_example.json",
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_tds2stacintegrator_nested_depth_gt_zero_without_webservice1():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario3/test/nested/first/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=1,
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_tds2stacintegrator_nested_depth_gt_zero_with_asset1():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario3/test/catalog.html",
        stac_dir="stac/",
        limited_number=1,
        depth_number=1,
        webservice_properties={
            "web_service_config_file": "./tag_example.json",
        },
        extension_properties={
            "item_extensions": [
                "common_metadata",
                "item_datacube_extension",
                (
                    "scientific_extension",
                    "item",
                    "./custom_based_on_defined_extension_pystac.py",
                ),
                (
                    "contact_extension",
                    "item",
                    "./custom_based_on_none_defined_extension_pystac.py",
                ),
            ],
        },
        asset_properties={
            # "item_thumbnail": True,
            # "item_getminmax_thumbnail": True,
            "explore_data": True,
            "verify_explore_data": True,
            "jupyter_notebook": True,
            "collection_thumbnail": "link",
            "collection_thumbnail_link": "https://images.fineartamerica.com/images-medium-large-5/global-precipitation-william-putmannasa-goddard-space-flight-center.jpg",
            "assets_list_allowed": ["wms", "wcs", "wfs"],
            "assets_list_avoided": ["http"],
            # "item_extra_custom_assets": [("extra_item_asset", "item_asset"),],
            # "extra_custom_assets":[{"href": "", "title": "", "description": "", "media_type": "", "roles": "", "extra_fields": ""},],
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )


# none nested depth = 0
def test_tds2stacintegrator_none_nested_depth_zero_all_possible_extensions():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=1,
        depth_number=0,
        extension_properties={
            "item_extensions": [
                "common_metadata",
                "item_datacube_extension",
                (
                    "scientific_extension",
                    "item",
                    "./custom_based_on_defined_extension_pystac.py",
                ),
                (
                    "contact_extension",
                    "item",
                    "./custom_based_on_none_defined_extension_pystac.py",
                ),
            ],
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_tds2stacintegrator_none_nested_depth_zero_with_webservice():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=0,
        webservice_properties={
            "web_service_config_file": "./tag_example.json",
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_tds2stacintegrator_none_nested_depth_zero_without_webservice():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        stac_dir="stac/",
        limited_number=2,
        depth_number=0,
        logger_properties={"logger_handler": "StreamHandler"},
    )


# def test_tds2stacintegrator_none_nested_depth_zero_with_asset():
#     TDS2STACIntegrator(
#         "http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html?dataset=a5f5be12-e4de-4977-adb7-a06480f65f48/2020336.nc",
#         stac_dir="stac/",
#         limited_number=1,
#         depth_number=0,
#         webservice_properties={
#             "web_service_config_file": "./tag_example.json",
#         },
#         extension_properties={
#             "item_extensions": [
#                 "common_metadata",
#                 "item_datacube_extension",
#                 (
#                     "scientific_extension",
#                     "item",
#                     "./custom_based_on_defined_extension_pystac.py",
#                 ),
#                 (
#                     "contact_extension",
#                     "item",
#                     "./custom_based_on_none_defined_extension_pystac.py",
#                 ),
#             ],
#         },
#         asset_properties={
#             "item_thumbnail": True,
#             "item_getminmax_thumbnail": True,
#             "explore_data": True,
#             "verify_explore_data": True,
#             "jupyter_notebook": True,
#             "collection_thumbnail": "wms",
#             "assets_list_allowed": ["wms", "wcs", "wfs"],
#             "assets_list_avoided": ["http"],
#             # "item_extra_custom_assets": [("extra_item_asset", "item_asset"),],
#             # "extra_custom_assets":[{"href": "", "title": "", "description": "", "media_type": "", "roles": "", "extra_fields": ""},],
#         },
#         logger_properties={"logger_handler": "NullHandler"},
#     )


def test_tds2stacintegrator_atmohub_linestring():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/main.html?dataset=f3627295-28e0-48a2-b9b5-c2bdac5fb2cf",
        stac_dir="stac/",
        stac_existence=True,
        stac_existence_collection=True,
        item_geometry_linestring=True,
        limited_number=2,
        depth_number=0,
        webservice_properties={
            "webservice": "all",
            "web_service_config_file": "./tag_example.json",
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_tds2stacintegrator_atmohub_point():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/main.html?dataset=a964b0f6-321e-481e-a43b-f036dd333ae2",
        stac_dir="stac/",
        stac_existence=True,
        stac_existence_collection=True,
        limited_number=2,
        depth_number=0,
        webservice_properties={
            "webservice": "all",
            "web_service_config_file": "./tag_example.json",
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )


# TODO: fix this test
def test_tds2stacintegrator_atmohub_spatial_information():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/main.html?dataset=a964b0f6-321e-481e-a43b-f036dd333ae2",
        stac_dir="stac/",
        stac_existence=True,
        stac_existence_collection=True,
        item_geometry_linestring=True,
        spatial_information=[0, 0, 0, 0],
        limited_number=2,
        depth_number=0,
        webservice_properties={
            "web_service_config_file": "./tag_example.json",
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_tds2stacintegrator_agg():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario7.html?dataset=2786bf07-8e3b-44d3-82bd-ee27024751ec",
        stac_dir="stac/",
        stac_existence=True,
        stac_existence_collection=True,
        aggregated_dataset_url="https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/regional/eobs/v27.0e/catalog.html",
        limited_number=2,
        collection_tuples=[
            (
                "catalog_catalogues_climate_catalog_ext_html_dataset_eobs_daily_0_1_aggregated_v27_aggregated",
                "sfsvs",
                "sadsdsdf",
                "dassdsdsfd",
            )
        ],
        depth_number=0,
        webservice_properties={
            "web_service_config_file": "./tag_example.json",
        },
        logger_properties={"logger_handler": "StreamHandler"},
    )


def test_tds2stacintegrator_empty():
    TDS2STACIntegrator(
        "http://localhost:8080/thredds/catalog/catalogs/scenario4.html",
        stac_dir="stac/",
        collection_tuples=[
            (
                "catalog_catalogues_bio_geo_chem_catalog_ext_html_empty",
                "sfsvs",
                "sadsdsdf",
                "dassdsdsfd",
            )
        ],
        logger_properties={"logger_handler": "StreamHandler"},
    )


# TODO: fix this test
def test_tds2stacintegrator_error():
    TDS2STACIntegrator(
        "https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/atmos_obs/lidar/Data/20220714/catalog.html?dataset=lidar/Data/20220714/e2271407.590015",
        stac_dir="stac/",
        logger_properties={"logger_handler": "StreamHandler"},
    )


# TODO: fix this test
def test_tds2stacintegrator_no_spatial_no_temporal():
    TDS2STACIntegrator(
        "https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/regional/seas5_bc/forecast_measures/raster/catalog.html",
        stac_dir="stac/",
        limited_number=1,
        logger_properties={"logger_handler": "StreamHandler"},
    )
