import os
from datetime import datetime

# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
import pystac

from .. import utils

unidata = "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0"
w3 = "http://www.w3.org/1999/xlink"
iso_gmd = "http://www.isotc211.org/2005/gmd"
iso_gco = "http://www.isotc211.org/2005/gco"
iso_gml = "http://www.opengis.net/gml/3.2"
global_bounding_box = [-360, -90, 0, 90]
No_inf = "No information"
ncml = "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2"
wms = "http://www.opengis.net/wms"
# a list of parameters to be not used in 'aName' parameter in iso webservice and 'dimension' and 'variable' parameters in ncML webservice
avoided_list = ["time_bnds", "bnds", "ens"]
# a list of parameters to be used in 'keyword' parameter in iso webservice
allowed_list = [
    "time",
    "lat",
    "latitude",
    "lon",
    "longitude",
    "long",
    "time_bnds",
    "bnds",
]
# a list of parameters to avoid use of them in final item
avoided_formats = [
    "float",
    "double",
    "int",
    "time_bnds",
    "bnds",
    "ens",
    "String",
    "short",
]
# Default value for having a bounding box for time-series data.
epilon = 0.000001


# webservice types that TDS2STAC supports
webservices_list = ["ncml", "wms", "iso"]
# List of array value attributes in `auto_switch_harvester`
append_list = ["keyword", "var_lists", "var_descs", "var_dims"]
# List of single value attributes in `auto_switch_harvester`
constant_list = [
    "long_min",
    "long_max",
    "lat_min",
    "lat_max",
    "time_start",
    "time_end",
]
# In the loop of 'auto_switch_harvester', criteria for locating the correct tag.
webservices_constants = dict(
    iso={
        "long_min": "{%s}westBoundLongitude_long_min" % iso_gmd,
        "long_max": "{%s}eastBoundLongitude_long_max" % iso_gmd,
        "lat_min": "{%s}southBoundLatitude_lat_min" % iso_gmd,
        "lat_max": "{%s}northBoundLatitude_lat_max" % iso_gmd,
        "keyword": "{%s}dimensionName_keyword" % iso_gmd,
        "var_lists": "{%s}MemberName_var_lists" % iso_gco,
        "var_descs": "{%s}descriptor_var_descs" % iso_gmd,
        "var_dims": "{%s}dimensionName_var_dims" % iso_gmd,
        "time_start": "{%s}beginPosition_time_start" % iso_gml,
        "time_end": "{%s}endPosition_time_end" % iso_gml,
    },
    ncml={
        "long_min": "geospatial_lon_min_long_min",
        "long_max": "geospatial_lon_max_long_max",
        "lat_min": "geospatial_lat_min_lat_min",
        "lat_max": "geospatial_lat_max_lat_max",
        "keyword": "{%s}variable_keyword" % ncml,
        "var_lists": "{%s}variable_var_lists" % ncml,
        "var_descs": "{%s}variable_var_descs" % ncml,
        "var_dims": "{%s}dimension_var_dims" % ncml,
        "time_start": "time_coverage_start_time_start",
        "time_end": "time_coverage_end_time_end",
    },
    wms={
        "long_min": "{%s}westBoundLongitude_long_min" % wms,
        "long_max": "{%s}eastBoundLongitude_long_max" % wms,
        "lat_min": "{%s}southBoundLatitude_lat_min" % wms,
        "lat_max": "{%s}northBoundLatitude_lat_max" % wms,
        "keyword": "{%s}Layer_keyword" % wms,
        "var_lists": "{%s}Layer_var_lists" % wms,
        "var_descs": "{%s}Layer_var_descs" % wms,
        "var_dims": "{%s}Layer_var_dims" % wms,
        "time_start": "{%s}Dimension_time_start" % wms,
        "time_end": "{%s}Dimension_time_end" % wms,
    },
)

schemas_dicts = {
    "catalog": "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0",
    "dap4": "http://xml.opendap.org/ns/DAP/4.0#",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "gco": "http://www.isotc211.org/2005/gco",
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gmi": "http://www.isotc211.org/2005/gmi",
    "srv": "http://www.isotc211.org/2005/srv",
    "gmx": "http://www.isotc211.org/2005/gmx",
    "gsr": "http://www.isotc211.org/2005/gsr",
    "gss": "http://www.isotc211.org/2005/gss",
    "gts": "http://www.isotc211.org/2005/gts",
    "gml": "http://www.opengis.net/gml/3.2",
    "xs": "http://www.w3.org/2001/XMLSchema",
    "ncml": "http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2",
    "wms": "http://www.opengis.net/wms",
    "xlink": "http://www.w3.org/1999/xlink",
    "edal": "http://reading-escience-centre.github.io/edal-java/wms",
}


static_list_webservices = [
    "tds2stac_mode_analyser",
    "tds2stac_manual_variable",
    "tds2stac_webservice_analyser",
    "tds2stac_reference_key",
]

default_tag_config_file = (
    os.path.dirname(os.path.abspath(utils.__file__)) + "/tag_config.json"
)
webservices_constants = dict(
    iso={
        "long_min": "{%s}westBoundLongitude_long_min" % iso_gmd,
        "long_max": "{%s}eastBoundLongitude_long_max" % iso_gmd,
        "lat_min": "{%s}southBoundLatitude_lat_min" % iso_gmd,
        "lat_max": "{%s}northBoundLatitude_lat_max" % iso_gmd,
        "keyword": "{%s}dimensionName_keyword" % iso_gmd,
        "var_lists": "{%s}MemberName_var_lists" % iso_gco,
        "var_descs": "{%s}descriptor_var_descs" % iso_gmd,
        "var_dims": "{%s}dimensionName_var_dims" % iso_gmd,
        "time_start": "{%s}beginPosition_time_start" % iso_gml,
        "time_end": "{%s}endPosition_time_end" % iso_gml,
    },
    ncml={
        "long_min": "geospatial_lon_min_long_min",
        "long_max": "geospatial_lon_max_long_max",
        "lat_min": "geospatial_lat_min_lat_min",
        "lat_max": "geospatial_lat_max_lat_max",
        "keyword": "{%s}variable_keyword" % ncml,
        "var_lists": "{%s}variable_var_lists" % ncml,
        "var_descs": "{%s}variable_var_descs" % ncml,
        "var_dims": "{%s}dimension_var_dims" % ncml,
        "time_start": "time_coverage_start_time_start",
        "time_end": "time_coverage_end_time_end",
    },
    wms={
        "long_min": "{%s}westBoundLongitude_long_min" % wms,
        "long_max": "{%s}eastBoundLongitude_long_max" % wms,
        "lat_min": "{%s}southBoundLatitude_lat_min" % wms,
        "lat_max": "{%s}northBoundLatitude_lat_max" % wms,
        "keyword": "{%s}Layer_keyword" % wms,
        "var_lists": "{%s}Layer_var_lists" % wms,
        "var_descs": "{%s}Layer_var_descs" % wms,
        "var_dims": "{%s}Layer_var_dims" % wms,
        "time_start": "{%s}Dimension_time_start" % wms,
        "time_end": "{%s}Dimension_time_end" % wms,
    },
)


colorbars = [
    "alg",
    "alg-inv",
    "alg2",
    "alg2-inv",
    "bluered_colorbrewer",
    "bluered_colorbrewer-inv",
    "cdi",
    "cdi-inv",
    "default",
    "default-inv",
    "div-BrBG",
    "div-BrBG-inv",
    "div-BuRd",
    "div-BuRd-inv",
    "div-BuRd2",
    "div-BuRd2-inv",
    "div-PRGn",
    "div-PRGn-inv",
    "div-PiYG",
    "div-PiYG-inv",
    "div-PuOr",
    "div-PuOr-inv",
    "div-RdBu",
    "div-RdBu-inv",
    "div-RdGy",
    "div-RdGy-inv",
    "div-RdYlBu",
    "div-RdYlBu-inv",
    "div-RdYlGn",
    "div-RdYlGn-inv",
    "div-Spectral",
    "div-Spectral-inv",
    "ferret",
    "ferret-inv",
    "greyscale",
    "greyscale-inv",
    "lai",
    "lai-inv",
    "ncview",
    "ncview-inv",
    "ndvi",
    "ndvi-inv",
    "npp",
    "npp-inv",
    "npp_sv",
    "npp_sv-inv",
    "occam",
    "occam-inv",
    "occam_pastel-30",
    "occam_pastel-30-inv",
    "precip",
    "precip-inv",
    "psu-inferno",
    "psu-inferno-inv",
    "psu-magma",
    "psu-magma-inv",
    "psu-plasma",
    "psu-plasma-inv",
    "psu-viridis",
    "psu-viridis-inv",
    "redblue",
    "redblue-inv",
    "redblue_colorbrewer",
    "redblue_colorbrewer-inv",
    "seq-BkBu",
    "seq-BkBu-inv",
    "seq-BkGn",
    "seq-BkGn-inv",
    "seq-BkRd",
    "seq-BkRd-inv",
    "seq-BkYl",
    "seq-BkYl-inv",
    "seq-BlueHeat",
    "seq-BlueHeat-inv",
    "seq-Blues",
    "seq-Blues-inv",
    "seq-BuGn",
    "seq-BuGn-inv",
    "seq-BuPu",
    "seq-BuPu-inv",
    "seq-BuYl",
    "seq-BuYl-inv",
    "seq-GnBu",
    "seq-GnBu-inv",
    "seq-Greens",
    "seq-Greens-inv",
    "seq-Greys",
    "seq-Greys-inv",
    "seq-GreysRev",
    "seq-GreysRev-inv",
    "seq-Heat",
    "seq-Heat-inv",
    "seq-OrRd",
    "seq-OrRd-inv",
    "seq-Oranges",
    "seq-Oranges-inv",
    "seq-PuBu",
    "seq-PuBu-inv",
    "seq-PuBuGn",
    "seq-PuBuGn-inv",
    "seq-PuRd",
    "seq-PuRd-inv",
    "seq-Purples",
    "seq-Purples-inv",
    "seq-RdPu",
    "seq-RdPu-inv",
    "seq-Reds",
    "seq-Reds-inv",
    "seq-YlGn",
    "seq-YlGn-inv",
    "seq-YlGnBu",
    "seq-YlGnBu-inv",
    "seq-YlOrBr",
    "seq-YlOrBr-inv",
    "seq-YlOrRd",
    "seq-YlOrRd-inv",
    "seq-cubeYF",
    "seq-cubeYF-inv",
    "sld",
    "sld-inv",
    "sld2",
    "sld2-inv",
    "sm_categ_extreme",
    "sm_categ_extreme-inv",
    "sm_categ_quintile",
    "sm_categ_quintile-inv",
    "sm_categ_tercile",
    "sm_categ_tercile-inv",
    "smi",
    "smi-inv",
    "spi",
    "spi-inv",
    "spi_alternative",
    "spi_alternative-inv",
    "sst_36",
    "sst_36-inv",
    "temp_categ_extreme",
    "temp_categ_extreme-inv",
    "temp_categ_quintile",
    "temp_categ_quintile-inv",
    "temp_categ_tercile",
    "temp_categ_tercile-inv",
    "test3",
    "test3-inv",
    "tp_above_probab",
    "tp_above_probab-inv",
    "tp_below_probab",
    "tp_below_probab-inv",
    "tp_categ_extreme",
    "tp_categ_extreme-inv",
    "tp_categ_quintile",
    "tp_categ_quintile-inv",
    "tp_categ_tercile",
    "tp_categ_tercile-inv",
    "tp_extreme_dry_probab",
    "tp_extreme_dry_probab-inv",
    "tp_extreme_wet_probab",
    "tp_extreme_wet_probab-inv",
    "whiteblue10",
    "whiteblue10-inv",
    "whitered10",
    "whitered10-inv",
    "wms_precip",
    "wms_precip-inv",
    "x-Ncview",
    "x-Ncview-inv",
    "x-Occam",
    "x-Occam-inv",
    "x-Rainbow",
    "x-Rainbow-inv",
    "x-Sst",
    "x-Sst-inv",
]

# harvesting_vars = {  # type: ignore
#     "item_id": None,
#     "long_min": None,
#     "long_max": None,
#     "lat_min": None,
#     "lat_max": None,
#     "keyword": [],  # dimension of each variable
#     "var_lists": [],
#     "var_descs": [],
#     "var_dims": [],
#     "time_start": None,
#     "time_end": None,
#     "modified_date_time": None,
#     "collection_interval_time": [],
#     "collection_interval_time_final": [],
#     "item_bbox": [],
#     "item_footprint": None,
#     "collection_bbox": [],
#     "collection_footprint": None,
#     "collection_footprint_point": None,
#     "services": [],
#     "dataset": None,
#     "catalog_url": None,
#     "catalog_id": None,
# }


harvesting_vars = {  # type: ignore
    "item_id": None,
    "description": None,
    "horizontal_ids_lat": None,
    "horizontal_ids_lon": None,
    "horizontal_axis_x": None,
    "horizontal_axis_y": None,
    "horizontal_extent_lon_min": None,
    "horizontal_extent_lon_max": None,
    "horizontal_extent_lat_min": None,
    "horizontal_extent_lat_max": None,
    "horizontal_description_lon": None,
    "horizontal_description_lat": None,
    "horizontal_reference_system": None,
    "vertical_ids": None,
    "vertical_axis": None,
    "vertical_extent_upper": None,
    "vertical_extent_lower": None,
    "vertical_description": None,
    "temporal_id": None,
    "temporal_axis": None,
    "temporal_extent_start_datetime": None,
    "temporal_extent_end_datetime": None,
    "temporal_description": None,
    "variable_description": [],  # Description of each variable
    "variable_dimensions": [],  # dimension of each variable
    "variable_ids": [],  # Variable names
    "variable_unit": [],  # Variable units
    "variable_types": None,  # Variable types
    "services": [],
    "dataset": None,
    "catalog_url": None,
    "main_dataset_url": None,
    "catalog_id": None,
    "item_bbox": [],
    "item_footprint": None,
    "collection_bbox": [],
    "collection_footprint": None,
    "collection_footprint_point": None,
    "collection_interval_time": [],
    "modified_date_time": None,
    "collection_interval_time_final": [],
}

nested_scenarios = [
    "First Scenario",
    "Third Scenario",
    "Second Scenario",
    "Eighth Scenario",
    "Ninth Scenario",
]
none_nested_scenarios = [
    "Fourth Scenario",
    "Fifth Scenario",
    "Sixth Scenario",
    "Seventh Scenario",
]
supported_webservices = [
    "ncml",
    "wms",
    "iso",
    "dap4",
    "NCML",
    "WMS",
    "ISO",
    "DAP4",
    "catalog",
    "all",
]
webservice_properties_main_keys = ["webservice"]
empty_collection = pystac.Collection(
    id="an-empty-collection-id",
    description="An Empty collection description",
    extent=pystac.Extent(
        spatial=pystac.SpatialExtent(bboxes=[0.0, 0.0]),
        temporal=pystac.TemporalExtent(
            intervals=[[datetime.utcnow(), datetime.utcnow()]]
        ),
    ),
)


default_extra_metadata_file = (
    os.path.dirname(os.path.abspath(utils.__file__)) + "/extra_metadata.json"
)
