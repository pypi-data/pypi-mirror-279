# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: EUPL-1.2
# isort: skip_file

"""TDS2STAC

TDS2STAC
"""

__all__ = [
    "__version__",
    "TDS2STACIntegrator",
    "Logger",
    "JSONFileWebServiceListScraper",
    "WebServiceListScraper",
    "WebServiceContentScraper",
    "ExistenceValidator",
    "CollectionHarvester",
    "ItemHarvester",
    "STACCreator",
    "NestedCollectionInspector",
    "Recognizer",
    "Spatial",
    "Temporal",
    "Datacube",
    "Verifier",
    "Thumbnails",
]

from . import _version

from tds2stac.tds2stac import TDS2STACIntegrator

from tds2stac.analysers.existence_validator import ExistenceValidator
from tds2stac.logger import Logger

from tds2stac.webservices.core import (
    JSONFileWebServiceListScraper,
    WebServiceContentScraper,
    WebServiceListScraper,
)

from tds2stac.harvester import CollectionHarvester

from tds2stac.harvester import ItemHarvester

from tds2stac.creator import STACCreator

from tds2stac.analysers.nested_collections import NestedCollectionInspector
from tds2stac.analysers.recognizer import Recognizer
from tds2stac.dimensions.spatial import Spatial
from tds2stac.dimensions.temporal import Temporal

from tds2stac.extensions.datacube import Datacube
from tds2stac.analysers.properties_verifier import Verifier
from tds2stac.thumbnails import Thumbnails


__version__ = _version.get_versions()["version"]

__author__ = "Mostafa Hadizadeh"
__copyright__ = "2023 Karlsruher Institut für Technologie"
__credits__ = [
    "Mostafa Hadizadeh",
]
__license__ = "EUPL-1.2"

__maintainer__ = "Mostafa Hadizadeh"
__email__ = "mostafa.hadizadeh@kit.edu"

__status__ = "Pre-Alpha"

from . import _version

__version__ = _version.get_versions()["version"]
