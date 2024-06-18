# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2

"""Test file for imports."""


def test_package_import():
    """Test the import of the main package."""
    import tds2stac  # noqa: F401
    from tds2stac.analysers.existence_validator import (  # noqa: F401
        ExistenceValidator,
    )
    from tds2stac.analysers.nested_collections import (  # noqa: F401
        NestedCollectionInspector,
    )
    from tds2stac.analysers.properties_verifier import Verifier  # noqa: F401
    from tds2stac.analysers.recognizer import Recognizer  # noqa: F401
    from tds2stac.creator import STACCreator  # noqa: F401
    from tds2stac.dimensions.spatial import Spatial  # noqa: F401
    from tds2stac.dimensions.temporal import Temporal  # noqa: F401
    from tds2stac.extensions.datacube import Datacube  # noqa: F401
    from tds2stac.harvester import CollectionHarvester  # noqa: F401
    from tds2stac.harvester import ItemHarvester  # noqa: F401
    from tds2stac.logger import Logger  # noqa: F401
    from tds2stac.tds2stac import TDS2STACIntegrator  # noqa: F401
    from tds2stac.thumbnails import Thumbnails  # noqa: F401
    from tds2stac.webservices.core import (  # noqa: F401
        JSONFileWebServiceListScraper,
        WebServiceContentScraper,
        WebServiceListScraper,
    )
