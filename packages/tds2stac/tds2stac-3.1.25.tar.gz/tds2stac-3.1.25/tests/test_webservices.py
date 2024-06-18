# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
from tds2stac import WebServiceListScraper


def test_WebServiceListScraper():
    WebServiceListScraper(
        url="http://localhost:8080/thredds/catalog/catalogs/scenario5/test/catalog.html",
        logger_properties={"logger_handler": "StreamHandler"},
        requests_properties={"timeout": 10, "verify": False},
    )
