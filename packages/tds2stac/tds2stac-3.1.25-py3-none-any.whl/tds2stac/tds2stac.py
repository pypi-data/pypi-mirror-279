import os

# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
import sys
import traceback
from datetime import datetime
from typing import Literal, Union

import pytz
import urllib3
from lxml import etree
from tqdm import tqdm

from . import assets, creator, harvester, logger, utils
from .analysers.nested_collections import NestedCollectionInspector
from .analysers.properties_verifier import Verifier
from .analysers.recognizer import Recognizer
from .statics import constants
from .webservices import core

##################################################
# Disabling the warning of InsecureRequestWarning
# for web server that doesn't have SSL certificate
##################################################
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TDS2STACIntegrator(object):
    """
    This class is the central component of the TDS2STAC. It harvests the TDS catalog
    and then generates the STAC-Catalog, -Collections, and -Items through the TDS catalogs,
    based on the user's input.
    This class mainly defines all configurations related to harvesting and STAC creation.
    In the first step, it recognizes the scenario of the TDS catalog using :class:`~tds2stac.Recognizer`.
    If it is recognized as a nested collection, :class:`~tds2stac.NestedCollectionInspector` is responsible for
    determining the nested collection's `ID`, `Title`, and `url` of subdirectories. Other procedures follow
    in succession. For example, :class:`~tds2stac.CollectionHarvester` harvests the collection's information
    and :class:`~tds2stac.STACCreator` creates the STAC-Catalog and -Collection. Then, :class:`~tds2stac.ItemHarvester`
    harvests the item's information and :class:`~tds2stac.STACCreator` creates the STAC-Item and connect them
    to the related STAC-Collections. At the end each STAC-Collection will be connected to the main STAC-Catalog.

    Args:
        TDS_catalog(str) : The URL address of the TDS catalog that will be harvested.
        stac_dir (str, Optional) : Directory of saving created STAC catalogs.
        stac_id (str, Optional): STAC catalog ID. default value is 'TDS2STAC'.
        stac_title (str, optional): STAC catalog Title. default value is 'TDS2STAC'.
        stac_description (str, optional): STAC catalog description.
        stac_existence (bool, optional): Verifying the presence of the STAC catalog in order to
            update an existing catalog; if not, a new catalog will be generated.
        stac_existence_collection (bool, optional): Verifying the presence of the STAC Collection
            in order to update an existing catalog; if not, a new collection will be generated.
        collection_tuples (list, optional): The elements of this tuple comprise the auto-TDS2STAC-generated ID
            , the user-defined ID, title, and description of the STAC-Collection respectively. (auto-ID, user-ID,
            user-title, user-description).
        datetime_filter (list, optional): Datetime-based filtering of harvesting. It works based on the `modified`
            tag in each dataset at TDS.
        aggregated_dataset_url (str, optional): Dataset's URL of each data entry in the Aggregated datasets of TDS.
        depth_number (int, optional) : depth number of nested datasets if it is a nested collection. default value is 0.
        limited_number (int, optional): The objective is to reduce the quantity of harvested items in each collection. It is beneficial
            for developing and testing purposes.
        spatial_information (list, optional): Spatial information of 2D datasets e.g. [minx, maxx, miny, maxy] or 1D dataset e.g.
            [x,y]. default value is None.
        temporal_format_by_dataname (str, optional): A preferred datetime format for datasets that include the time period in their names. e.g
            "e%y%m%d%H.%M%S%f"
        item_geometry_linestring (bool, optional): Set True to make a LineString geometry for STAC-Items from wms service.
            Otherwise it makes Polygon geometry for the given Item. default value is False.
        extension_properties (dict, optional): A dictionary of properties for extensions. default is None.
            For more information about the keys, please refer to the :class:`~tds2stac.TDS2STACIntegrator.extension_properties`.
        webservice_properties (dict, optional): A dictionary of properties for web_service. default is None (optional)
            For more information about the keys, please refer to the :class:`~tds2stac.TDS2STACIntegrator.webservice_properties`.
        asset_properties (dict, optional): A dictionary of properties for assets. default is None (optional)
            For more information about the keys, please refer to the :class:`~tds2stac.TDS2STACIntegrator.asset_properties`.
        logger_properties (dict, optional): A dictionary of properties for logger. default is `None`.
        requests_properties (dict, optional): A dictionary that modify the requests to
            URLs. To obtain additional information on this topic, refer to
            the :class:`~tds2stac.TDS2STAC.requests_properties`. The default value is
            an empty dictionary.
       extra_metadata (dict, optional): A dictionary of extra metadata that
            you desire to include in the STAC-Collection and STAC-Items. To obtain
            additional information on this topic, please refer to the
            :class:`~tds2stac.TDS2STAC.extra_metadata`. The default value is an empty
            dictionary


    """

    TDS_catalog: str
    """
        TDS catalog URL address. Initial point of harvesting e.g.
        https://thredds.atmohub.kit.edu/thredds/catalog/caribic/IAGOS-CARIBIC_MS_files_collection_20231017/catalog.html
    """
    stac_dir: str
    """
    Directory of saving created STAC catalogs e.g. /path/to/stac/directory/
    """
    stac_id: str
    """
    STAC catalog ID. default value `TDS2STAC`
    """
    stac_title: Union[str, None]
    """
    STAC catalog Title. default value `TDS2STAC`
    """
    stac_description: Union[str, None]
    """
    STAC catalog description
    """
    stac_existence: Literal[False]
    """
    Verifying the existence of STAC catalog.
    If the catalog exists in the directory, it updates a existed catalog,
    otherwise it creates new catalog. default value `False`
    """
    stac_existence_collection: Literal[False]
    """
    Verifying the existence of STAC Collections.
    If the collection exists in the directory, it updates a existed collection,
    otherwise it creates new collection. default value `False`
    """
    collection_tuples: Union[list[tuple], None]
    """
    STAC collection auto-generated ID, user-ID, user-Title and user-Description defined by user.
    It is worth mentioning that in order to obtain the list of automatically generated collection
    IDs, one can employ the :class:`~tds2stac.NestedCollectionInspector` for the given
    TDS Catalog and subsequently utilize this argument.
    Warning - Identifiers should consist of only lowercase characters, numbers, '_', and '-'.
    Default value `None`. e.g. (ID, Title, Description)
    """
    datetime_filter: Union[list, None]
    """
    Datetime-based filtering. e.g. ``['2010-02-18T00:00:00.000Z','2020-02-22T00:00:00.000Z']``
    Default value `None`. It should be noted it works based on the `modified` tag in each dataset at TDS.
    """
    aggregated_dataset_url: Union[str, None]
    """
    Dataset's URL of each data entry in the Aggregated datasets of TDS.. default value `None`.
    The `HTTPServer` is not functional in the aggregated dataset. Therefore, in order to utilize
    this service as an asset in our STAC-Item, we should employ the `aggregated_dataset_url`, which
    links the individual datasets to the `HTTPServer` asset of the relevant Item.
    """
    depth_number: Union[int, None]
    """
    The depth refers to the number of layered datasets. If the collection is nested, this argument
    is applicable; otherwise, employing this argument would be futile. default value `None` (optional)
    """
    limited_number: Union[int, None]
    """
    The objective is to reduce the quantity of harvested items in each collection. It is beneficial
    for developing and testing purposes.. default value `None` (optional)
    """
    spatial_information: Union[list, None]
    """
    Spatial information of 2D datasets e.g. [minx, maxx, miny, maxy] or 1D dataset e.g. [x,y].
    Default value `None`(optional)
    """
    temporal_format_by_dataname: Union[str, None]
    """
    A preferred datetime format for datasets that include the time period in their names e.g "e%y%m%d%H.%M%S%f".
    Default value `None` (optional)
    """
    item_geometry_linestring: Literal[False]
    """
    The default value for the LineString geometry in the STAC Items from the WMS
    service is set to False and the default geometry type for the STAC-Item is Polygon.
    However, in instances where the item has a POINT geometry, it can be automatically detected.
    However, in order to obtain the LineString geometry, it is necessary to set this argument
    to True.
    """
    extension_properties: Union[dict, None]
    """
    A dictionary of properties for extensions. default is `None`.

        **item_extensions (list[str, tuple], optional)**:
            The argument can consist of either a list of extension names (string) or a
            list of tuples containing three elements: the extension name, the function
            name or class name associated with the extension, and the Python script
            required for execution. For more explanation, refer to the :ref:`custom-extension`.

        **collection_extensions (Union[list, tuple], optional)**:
            It works as same as `item_extensions` argument. For more explanation,
            refer to the :ref:`custom-extension`.

    """

    webservice_properties: Union[dict, None]
    """
    A dictionary of properties for web_service. default is `None`.

    It has the following keys.
        **web_service_config_file(str, opntional)**:
            The primary `tag_config.json` file is situated in the primary directory
            of the installed TDS2STAC. However, the user has the ability to declare
            an alternative `tag_config.json` file, which allows for customization of
            the settings. The user can specify the location of their own JSON file
            in this section. To obtain further details on the creation of a
            `tag_config.json` file, refer: :ref:`tag-config`. The default
            value is set to `tag_config.json` in the root directory of the installed
            app.
    """
    asset_properties: Union[dict, None]
    """
    A dictionary of properties for assets. default is `None`.
    When it's None, keys look like the following example:
        **collection_thumbnail (str, optional)**:
            A `thumbnail` asset for STAC-collection sourced from the Web Map Service (WMS)
            of the TDS. It can be chosen from `wms`, `link`, or `None`. The default value
            is set to None.
        **collection_overview (str, optional)**:
            A `overview` asset for STAC-collection sourced from the Web Map Service (WMS)
            of the TDS. It can be chosen from `wms`, `link`, or `None`. The default value
            is set to None.
        **collection_thumbnail_link (str, optional)**:
            This property is reliant upon the values of `collection_thumbnail` and
            `collection_overview`. When the value of either of these attributes is
            set to `link`, it allows for the inclusion of a hyperlink to an image
            for `collection_thumbnail` or `collection_overview`.
        **collection_overview_link (str, optional)**:
            This property is reliant upon the values of `collection_thumbnail` and
            `collection_overview`. When the value of either of these attributes is
            set to `link`, it allows for the inclusion of a hyperlink to an image
            for `collection_thumbnail` or `collection_overview`.
        **collection_custom_assets (list, optional)**:
            This is a list of asset dictionaris that includes the `key`, `href`, and
            `title`, `role` (as a list), and `media_type` of the asset. The default
            value is set to None. For more information, refer to the :ref:`custom-asset`.
        **item_thumbnail (bool, optional)**:
            A `thumbnail` asset for STAC-Items sourced from the Web Map Service (WMS)
            of the TDS. The default value is set to False.
        **item_overview (bool, optional)**:
            A `overview` asset for STAC-Items sourced from the Web Map Service (WMS)
            of the TDS. The default value is set to False.
        **item_getminmax_thumbnail (bool, optional)**:
            The TDS offers a function that allows users to obtain the minimum and maximum
            values of the colorbar associated with an image through the use of `metadata`.
            The aforementioned attribute is contingent upon both the `item_thumbnail` and
            `item_overview`. The default value is set to False.
        **assets_list_allowed (list, optional)**:
            This is a list of permissible web services that will be incorporated as assets
            in the STAC-Item. The :class:`~tds2stac.WebServiceScraper` class provides access
            to the list of available web services. Default value is None.
        **assets_list_avoided (list, optional)**:
            This is a list of web services that will be excluded from the STAC-Item asset
            list. The :class:`~tds2stac.WebServiceScraper` class provides access to the
            list of available webservices. Default value is None.
        **explore_data (bool, optional)**:
            By enabling the `True` setting, the inclusion of Godiva3 as an exploration asset will be implemented.
        **verify_explore_data (bool, optional)**:
            This argument verifies the availability of the `GetMetadata` function. The provided
            function facilitates the retrieval of data necessary for generating maps using the
            Web Map Service (WMS) protocol. However, an error occurs when attempting to open
            `Godiva3` when this function doesn't work. In order to mitigate such errors, it
            would be advisable to establish this argument.
        **jupyter_notebook (bool, optional)**:
            This argument posits the inclusion of the Jupyter Notebook as an asset.
    """
    logger_properties: dict
    """
    A dictionary of properties for logger. default is `None`.
    You can look at keys in :class:`~tds2stac.logger.Logger` class.
    """
    requests_properties: dict
    """
    A dictionary of properties that adjust the requests to URLs. It contains the following keys:

        **verify (bool, optional)**:
            It is a boolean that if it is True, it verifies the SSL certificate. By default it is False.
        **timeout (int, optional)**:
            It is an integer that sets the timeout of the requests. By default it is 10 seconds.
        **auth (tuple, optional)**:
            It is a tuple that contains the username and password for the authentication. By default it is None.
    """
    extra_metadata: dict
    """
    A dictionary of extra metadata that you want to add to the
    STAC-Collection and STAC-Items. It has two main keys,
    `extra_metadata` that is boolean and `extra_metadata_file`
    that is the address of `extra_metadata.json` JSON file. For
    getting more information about making the `extra_metadata.json`
    file, please refer to :ref:`extra_metadata`.
    By default, if 'extra_metadata' is set to True, the
    'extra_metadata.json' file is utilised for the 'extra_metadata_file'
    key, which is situated in the'sta2stac' main directory.
    """

    def __init__(
        self,
        TDS_catalog: str,
        stac_dir: str = os.getcwd(),
        # web_service: str,
        stac_id: str = "TDS2STAC",
        stac_title: Union[str, None] = "TDS2STAC",
        stac_description: Union[str, None] = None,
        stac_existence: bool = False,
        stac_existence_collection: bool = False,
        collection_tuples: Union[list[tuple], None] = None,
        datetime_filter: Union[list, None] = None,
        aggregated_dataset_url: Union[str, None] = None,
        depth_number: Union[int, None] = None,
        limited_number: Union[int, None] = None,
        # spatial_information :Union[list[Union[str, int], Union[str, int]]|list[Union[str, int], Union[str, int],Union[str, int],Union[str, int]], None] = None,
        spatial_information: Union[list, None] = None,
        temporal_format_by_dataname: Union[str, None] = None,
        item_geometry_linestring: bool = False,
        webservice_properties: Union[dict, None] = dict(),
        asset_properties: Union[dict, None] = dict(),
        extension_properties: Union[dict, None] = dict(),
        logger_properties: dict = dict(),
        requests_properties: dict = dict(),
        extra_metadata: dict = dict(),
    ) -> None:
        ################################################
        # Verifying the `webservice_properties`,
        # `asset_properties`, and `extension_properties`,
        # when they are None
        ################################################
        verifier = Verifier()
        if webservice_properties is not None and isinstance(
            webservice_properties, dict
        ):
            verifier.webservice_properties(webservice_properties)
        if asset_properties is not None and isinstance(asset_properties, dict):
            verifier.asset_properties(asset_properties)
        if extension_properties is not None and isinstance(
            extension_properties, dict
        ):
            verifier.extension_properties(extension_properties)
        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            verifier.logger_properties(logger_properties)
        if (
            requests_properties is not None
            and requests_properties != {}
            and isinstance(requests_properties, dict)
        ):
            verifier.requests_properties(requests_properties)
            self.requests_properties = requests_properties
        self.requests_properties = requests_properties

        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            self.logger_properties = logger_properties
        if extra_metadata is not None and isinstance(extra_metadata, dict):
            verifier.extra_metadata(extra_metadata)

        self.logger_properties["logger_level"] = "DEBUG"
        self.logger_properties["logger_msg"] = "Harvesting is started!"
        logger.Logger(self.logger_properties)

        ################################################
        # Getting the list of used webservices names in
        # `tag_config.json`
        ################################################
        if webservice_properties is not None:
            if (
                webservice_properties.get("web_service_config_file")
                is not None
                and webservice_properties["web_service_config_file"]
                == "default"
            ):
                webservice_properties["webservices"] = list(
                    core.ConfigFileWebServicesScraper(
                        constants.default_tag_config_file,
                        self.logger_properties,
                    )
                )
            elif (
                webservice_properties["web_service_config_file"] is not None
                and webservice_properties["web_service_config_file"]
                != "default"
            ):
                webservice_properties["webservices"] = list(
                    core.ConfigFileWebServicesScraper(
                        webservice_properties["web_service_config_file"],
                        self.logger_properties,
                    )
                )
        ################################################
        # Defining a dict to store the items information
        ################################################
        item_harvested_details = None
        ################################################
        # Getting the Date time modiefied of TDS catalog
        ################################################
        if datetime_filter is not None:
            """Skip TDS datasets out of 'datetime_filter' according
            to 'modified' attribute in `date` tag"""

            if datetime_filter[0] is not None:
                try:
                    datetime_after = datetime.strptime(
                        datetime_filter[0], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )

                    if not isinstance(datetime_after, datetime):
                        self.logger_properties[
                            "logger_msg"
                        ] = "`datetime_after` parameter have to be a datatime object. Therefore `datetime_filter` is not applied for this harvesting."
                        self.logger_properties["logger_level"] = "WARNING"
                        logger.Logger(self.logger_properties)

                    else:
                        if datetime_after.tzinfo:
                            datetime_after = datetime_after.astimezone(
                                pytz.utc
                            )
                        else:
                            datetime_after = datetime_after.replace(
                                tzinfo=pytz.utc
                            )
                except Exception:
                    datetime_after = None
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    if ex_type is not None and ex_value is not None:
                        self.logger_properties[
                            "logger_msg"
                        ] = "`datetime_filter` warning: %s : %s" % (
                            ex_type.__name__,
                            ex_value,
                        )
                        self.logger_properties["logger_level"] = "WARNING"
                        logger.Logger(self.logger_properties)
                        print(traceback.format_exc())

            if datetime_filter[1] is not None:
                try:
                    datetime_before = datetime.strptime(
                        datetime_filter[1], "%Y-%m-%dT%H:%M:%S.%fZ"
                    )

                    if not isinstance(datetime_before, datetime):
                        self.logger_properties[
                            "logger_msg"
                        ] = "`datetime_before` parameter have to be a datatime object. Therefore `datetime_filter` is not applied for this harvesting."
                        self.logger_properties["logger_level"] = "WARNING"
                        logger.Logger(self.logger_properties)
                    else:
                        if datetime_before.tzinfo:
                            datetime_before = datetime_before.astimezone(
                                pytz.utc
                            )
                        else:
                            datetime_before = datetime_before.replace(
                                tzinfo=pytz.utc
                            )
                except Exception:
                    datetime_before = None
                    if ex_type is not None and ex_value is not None:
                        self.logger_properties[
                            "logger_msg"
                        ] = "`datetime_filter` warning: %s : %s" % (
                            ex_type.__name__,
                            ex_value,
                        )
                        self.logger_properties["logger_level"] = "WARNING"
                        logger.Logger(self.logger_properties)
                    print(traceback.format_exc())
        else:
            datetime_after = None
            datetime_before = None
        ###############################
        # Finding dataset's scenario
        ###############################
        recognizer = Recognizer(
            main_catalog_url=TDS_catalog,
            logger_properties=self.logger_properties,
            requests_properties=self.requests_properties,
        )
        ###############################
        # STAC-Catalog creation
        ###############################
        STAC_creator = creator.STACCreator()
        stac_catalog = STAC_creator.STACCatalog(
            url=TDS_catalog,
            stac_id=stac_id,
            stac_title=stac_title,
            stac_desc=stac_description,
            stac_dir=stac_dir,
            stac_existence=stac_existence,
            logger_properties=self.logger_properties,
            requests_properties=self.requests_properties,
        )
        validate_value = utils.validate_catalog_url(
            url=TDS_catalog, requests_properties=self.requests_properties
        )
        if not validate_value:
            self.logger_properties["logger_level"] = "CRITICAL"
            self.logger_properties[
                "logger_msg"
            ] = "The TDS catalog URL is not valid! Please check the URL and try again."
            logger.Logger(self.logger_properties)
            return
        else:
            self.logger_properties["logger_level"] = "DEBUG"
            self.logger_properties[
                "logger_msg"
            ] = "The TDS catalog URL is valid!"
            logger.Logger(self.logger_properties)
        ########################################
        # STAC-Collection and -Item creation
        # 1. Harvest for nested collections
        ########################################
        if any(
            scenario in str(recognizer.status)
            for scenario in constants.nested_scenarios
        ):
            list_of_collection_details = NestedCollectionInspector(
                main_catalog_url=TDS_catalog,
                nested_number=depth_number,
                logger_properties=self.logger_properties,
                requests_properties=self.requests_properties,
            )
            for k in list_of_collection_details:
                ###########################################
                # defining a new function that harvests the
                # collections and create STAC-Collections
                # - Harvest Collection's information
                ###########################################
                collection_dict = harvester.CollectionHarvester(
                    TDS_catalog,
                    recognizer.status,
                    subdirs=k,
                    collection_tuples=collection_tuples,
                    logger_properties=self.logger_properties,
                    requests_properties=self.requests_properties,
                )
                ###########################
                # - Create STAC-Collection
                ###########################
                stac_collection = STAC_creator.STACCollection(
                    catalog=stac_catalog,
                    collection_id=dict(collection_dict)["collection_id"],
                    collection_title=dict(collection_dict)["collection_title"],
                    collection_description=dict(collection_dict)[
                        "collection_description"
                    ],
                    stac_existence_collection=stac_existence_collection,
                    extra_metadata=extra_metadata,
                )
                ###########################################
                # - Loop over collection's items
                ###########################################
                if k[3] != []:
                    for url_for_items in k[3]:
                        (
                            xml_url_catalog,
                            id_catalog,
                            xml,
                        ) = utils.xml_processing(
                            url_for_items, self.requests_properties
                        )
                        recognizer_output = Recognizer(
                            main_catalog_url=xml_url_catalog,
                            logger_properties=self.logger_properties,
                            requests_properties=self.requests_properties,
                        )

                        try:
                            tree = etree.XML(xml)
                        except BaseException:
                            continue
                        data_counted: int = 0

                        for data in tqdm(
                            tree.findall(
                                ".//{%s}dataset[@urlPath]" % constants.unidata
                            ),
                            colour="red",
                        ):
                            data_counted += 1
                            if limited_number is not None:
                                if data_counted > limited_number:
                                    break
                            if (
                                utils.replacement_func_collection_item_id(
                                    utils.replacement_func(data.get("ID"))
                                )
                                in stac_collection["existed_items_id_list"]
                            ):
                                continue
                            self.harvesting_vars = constants.harvesting_vars
                            self.harvesting_vars[
                                "collection_interval_time"
                            ] = (  # noqa
                                dict(item_harvested_details)["collection_interval_time"] if item_harvested_details is not None else []  # type: ignore
                            )
                            self.harvesting_vars[
                                "collection_interval_time_final"
                            ] = (  # noqa
                                dict(item_harvested_details)["collection_interval_time_final"] if item_harvested_details is not None else []  # type: ignore
                            )
                            self.harvesting_vars["collection_bbox"] = (  # noqa
                                dict(item_harvested_details)["collection_bbox"] if item_harvested_details is not None else []  # type: ignore
                            )
                            self.harvesting_vars[
                                "collection_footprint"
                            ] = (  # noqa
                                dict(item_harvested_details)["collection_footprint"] if item_harvested_details is not None else None  # type: ignore
                            )
                            self.harvesting_vars["collection_footprint_point"] = dict(item_harvested_details)["collection_footprint_point"] if item_harvested_details is not None else None  # type: ignore
                            ################################
                            # - Harvest Item
                            #################################
                            item_harvested_details = harvester.ItemHarvester(
                                xml_url_catalog,
                                data,
                                self.harvesting_vars,
                                webservice_properties,
                                datetime_after=datetime_after,
                                datetime_before=datetime_before,
                                spatial_information=spatial_information,
                                temporal_format_by_dataname=temporal_format_by_dataname,
                                extension_properties=extension_properties,
                                linestring=item_geometry_linestring,
                                requests_properties=self.requests_properties,
                                logger_properties=self.logger_properties,
                            )

                            ################################
                            # - Create STAC-Item
                            #################################

                            STAC_creator.STACItem(
                                xml_url_catalog,
                                stac_catalog,
                                dict(item_harvested_details),
                                recognizer_output.status,
                                dict(collection_dict)["collection_id"],
                                aggregated_dataset_url=aggregated_dataset_url,
                                extension_properties=extension_properties,
                                asset_properties=asset_properties,
                                extra_metadata=extra_metadata,
                                stac_existence_collection=stac_existence_collection,
                                collection_bbox_existed=dict(stac_collection)[
                                    "collection_bbox_existed"
                                ],
                                collection_interval_time_final_existed=dict(
                                    stac_collection
                                )["collection_interval_time_final_existed"],
                                logger_properties=self.logger_properties,
                            )
                            if asset_properties is not None and (
                                asset_properties["collection_thumbnail"]
                                in [
                                    "wms",
                                    "link",
                                ]
                                or asset_properties["collection_overview"]
                                in ["wms", "link"]
                                or asset_properties.get(
                                    "collection_custom_asset"
                                )
                                is not None
                            ):
                                if (item_harvested_details) is not None:
                                    asset = assets.Assets()
                                    asset.collection(
                                        harvesting_vars=dict(
                                            item_harvested_details
                                        ),
                                        collection_dict=dict(collection_dict),
                                        stac_catalog=stac_catalog,
                                        asset_properties=asset_properties,
                                        logger_properties=self.logger_properties,
                                    )

                else:
                    (
                        xml_url_catalog,
                        id_catalog,
                        xml,
                    ) = utils.xml_processing(k[0], self.requests_properties)
                    recognizer_output = Recognizer(
                        main_catalog_url=xml_url_catalog,
                        logger_properties=self.logger_properties,
                        requests_properties=self.requests_properties,
                    )

                    try:
                        tree = etree.XML(xml)
                    except BaseException:
                        return
                    data_counted = 0
                    for data in tqdm(
                        tree.findall(
                            ".//{%s}dataset[@urlPath]" % constants.unidata
                        ),
                        colour="red",
                    ):
                        data_counted += 1
                        if limited_number is not None:
                            if data_counted > limited_number:
                                break
                        if (
                            utils.replacement_func_collection_item_id(
                                utils.replacement_func(data.get("ID"))
                            )
                            in stac_collection["existed_items_id_list"]
                        ):
                            continue

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
                            "variable_description": None,  # Description of each variable
                            "variable_dimensions": None,  # dimension of each variable
                            "variable_ids": None,  # Variable names
                            "variable_unit": None,  # Variable units
                            "variable_types": None,  # Variable types
                            "services": None,
                            "dataset": None,
                            "catalog_url": None,
                            "main_dataset_url": None,
                            "catalog_id": None,
                            "item_bbox": None,
                            "item_footprint": None,
                            "collection_bbox": None,
                            "collection_footprint": None,
                            "collection_footprint_point": None,
                            "collection_interval_time": None,
                            "modified_date_time": None,
                            "collection_interval_time_final": None,
                        }

                        harvesting_vars["collection_interval_time"] = (  # noqa
                            dict(item_harvested_details)["collection_interval_time"] if item_harvested_details is not None else []  # type: ignore
                        )
                        harvesting_vars[
                            "collection_interval_time_final"
                        ] = (  # noqa
                            dict(item_harvested_details)["collection_interval_time_final"] if item_harvested_details is not None else []  # type: ignore
                        )
                        harvesting_vars["collection_bbox"] = (  # noqa
                            dict(item_harvested_details)["collection_bbox"] if item_harvested_details is not None else []  # type: ignore
                        )
                        harvesting_vars["collection_footprint"] = (  # noqa
                            dict(item_harvested_details)["collection_footprint"] if item_harvested_details is not None else None  # type: ignore
                        )
                        harvesting_vars[
                            "collection_footprint_point"
                        ] = (  # noqa
                            dict(item_harvested_details)["collection_footprint_point"] if item_harvested_details is not None else None  # type: ignore
                        )
                        ################################
                        # - Harvest Item
                        #################################

                        item_harvested_details = harvester.ItemHarvester(
                            xml_url_catalog,
                            data,
                            harvesting_vars,
                            webservice_properties,
                            datetime_after=datetime_after,
                            datetime_before=datetime_before,
                            spatial_information=spatial_information,
                            temporal_format_by_dataname=temporal_format_by_dataname,
                            extension_properties=extension_properties,
                            linestring=item_geometry_linestring,
                            requests_properties=self.requests_properties,
                            logger_properties=self.logger_properties,
                        )

                        ################################
                        # - Create STAC-Item
                        #################################
                        STAC_creator.STACItem(
                            xml_url_catalog,
                            stac_catalog,
                            dict(item_harvested_details),
                            recognizer_output.status,
                            dict(collection_dict)["collection_id"],
                            aggregated_dataset_url=aggregated_dataset_url,
                            extension_properties=extension_properties,
                            asset_properties=asset_properties,
                            extra_metadata=extra_metadata,
                            stac_existence_collection=stac_existence_collection,
                            collection_bbox_existed=dict(stac_collection)[
                                "collection_bbox_existed"
                            ],
                            collection_interval_time_final_existed=dict(
                                stac_collection
                            )["collection_interval_time_final_existed"],
                            logger_properties=self.logger_properties,
                        )

                    if asset_properties is not None and (
                        asset_properties["collection_thumbnail"]
                        in [
                            "wms",
                            "link",
                        ]
                        or asset_properties["collection_overview"]
                        in ["wms", "link"]
                        or asset_properties.get("collection_custom_asset")
                        is not None
                    ):
                        if (item_harvested_details) is not None:
                            asset = assets.Assets()
                            asset.collection(
                                harvesting_vars=dict(item_harvested_details),
                                collection_dict=dict(collection_dict),
                                stac_catalog=stac_catalog,
                                asset_properties=asset_properties,
                                logger_properties=self.logger_properties,
                            )

        ########################################
        # 1. Harvest for none-nested collections
        ########################################
        else:
            ###########################################
            # defining a new function that harvests the
            # collections and create STAC-Collections
            # - Harvest Collection
            ###########################################

            collection_dict = harvester.CollectionHarvester(
                TDS_catalog,
                recognizer.status,
                subdirs=None,
                collection_tuples=collection_tuples,
                logger_properties=self.logger_properties,
                requests_properties=self.requests_properties,
            )
            ###########################
            # - Create STAC-Collection
            ###########################
            stac_collection = STAC_creator.STACCollection(
                catalog=stac_catalog,
                collection_id=dict(collection_dict)["collection_id"],
                collection_title=dict(collection_dict)["collection_title"],
                collection_description=dict(collection_dict)[
                    "collection_description"
                ],
                stac_existence_collection=stac_existence_collection,
                extra_metadata=extra_metadata,
            )
            ###########################################
            # - Loop over collection's items
            ###########################################
            (
                xml_url_catalog,
                id_catalog,
                xml,
            ) = utils.xml_processing(TDS_catalog, self.requests_properties)
            recognizer_output = Recognizer(
                main_catalog_url=xml_url_catalog,
                logger_properties=self.logger_properties,
                requests_properties=self.requests_properties,
            )
            try:
                tree = etree.XML(xml)
            except BaseException:
                return
            data_counted = 0

            for data in tqdm(
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata),
                colour="red",
            ):
                data_counted += 1
                if limited_number is not None:
                    if data_counted > limited_number:
                        break
                # if data_counted % 50 == 0:
                #     import gc
                #     gc.collect()
                #     del stac_catalog
                #     del stac_collection
                #     stac_catalog = None
                #     stac_collection = None
                #     stac_catalog = stac_catalog_temp
                #     stac_collection = stac_collection_temp

                if (
                    utils.replacement_func_collection_item_id(
                        utils.replacement_func(data.get("ID"))
                    )
                    in stac_collection["existed_items_id_list"]
                ):
                    continue
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
                    "variable_description": None,  # Description of each variable
                    "variable_dimensions": None,  # dimension of each variable
                    "variable_ids": None,  # Variable names
                    "variable_unit": None,  # Variable units
                    "variable_types": None,  # Variable types
                    "services": None,
                    "dataset": None,
                    "catalog_url": None,
                    "main_dataset_url": None,
                    "catalog_id": None,
                    "item_bbox": None,
                    "item_footprint": None,
                    "collection_bbox": None,
                    "collection_bbox_existed": None,
                    "collection_footprint": None,
                    "collection_footprint_point": None,
                    "collection_interval_time": None,
                    "modified_date_time": None,
                    "collection_interval_time_final": None,
                    "collection_interval_time_final_existed": None,
                }

                harvesting_vars["collection_interval_time"] = (  # noqa
                    dict(item_harvested_details)["collection_interval_time"] if item_harvested_details is not None else []  # type: ignore
                )
                harvesting_vars["collection_interval_time_final"] = (  # noqa
                    dict(item_harvested_details)["collection_interval_time_final"] if item_harvested_details is not None else []  # type: ignore
                )
                harvesting_vars["collection_bbox"] = (  # noqa
                    dict(item_harvested_details)["collection_bbox"] if item_harvested_details is not None else []  # type: ignore
                )
                harvesting_vars["collection_footprint"] = (  # noqa
                    dict(item_harvested_details)["collection_footprint"] if item_harvested_details is not None else None  # type: ignore
                )
                harvesting_vars["collection_footprint_point"] = (  # noqa
                    dict(item_harvested_details)["collection_footprint_point"] if item_harvested_details is not None else None  # type: ignore
                )
                ################################
                # - Harvest Item
                #################################

                item_harvested_details = harvester.ItemHarvester(
                    xml_url_catalog,
                    data,
                    harvesting_vars,
                    webservice_properties,
                    datetime_after=datetime_after,
                    datetime_before=datetime_before,
                    spatial_information=spatial_information,
                    temporal_format_by_dataname=temporal_format_by_dataname,
                    extension_properties=extension_properties,
                    linestring=item_geometry_linestring,
                    requests_properties=self.requests_properties,
                    logger_properties=self.logger_properties,
                )

                ################################
                # - Create STAC-Item
                #################################
                STAC_creator.STACItem(
                    xml_url_catalog,
                    stac_catalog,
                    dict(item_harvested_details),
                    recognizer_output.status,
                    dict(collection_dict)["collection_id"],
                    aggregated_dataset_url=aggregated_dataset_url,
                    extension_properties=extension_properties,
                    asset_properties=asset_properties,
                    extra_metadata=extra_metadata,
                    stac_existence_collection=stac_existence_collection,
                    collection_bbox_existed=dict(stac_collection)[
                        "collection_bbox_existed"
                    ],
                    collection_interval_time_final_existed=dict(
                        stac_collection
                    )["collection_interval_time_final_existed"],
                    logger_properties=self.logger_properties,
                )
                data.clear()
            if asset_properties is not None and (
                asset_properties["collection_thumbnail"]
                in [
                    "wms",
                    "link",
                ]
                or asset_properties["collection_overview"] in ["wms", "link"]
                or asset_properties.get("collection_custom_asset") is not None
            ):
                if (item_harvested_details) is not None:
                    asset = assets.Assets()
                    asset.collection(
                        harvesting_vars=dict(item_harvested_details),
                        collection_dict=dict(collection_dict),
                        stac_catalog=stac_catalog,
                        asset_properties=asset_properties,
                        logger_properties=self.logger_properties,
                    )

        #############################
        # Saving STAC catalog
        #############################
        self.logger_properties["logger_level"] = "DEBUG"
        self.logger_properties["logger_msg"] = "Harvesting is Finished!"
        logger.Logger(self.logger_properties)
        self.logger_properties["logger_level"] = "DEBUG"
        self.logger_properties[
            "logger_msg"
        ] = "Creating STAC-Metadata is started!"
        logger.Logger(self.logger_properties)

        save_out = STAC_creator.SaveCatalog(
            catalog=stac_catalog,
            catalog_dir=stac_dir,
            logger_properties=self.logger_properties,
        )
        if save_out:
            self.logger_properties["logger_level"] = "DEBUG"
            self.logger_properties[
                "logger_msg"
            ] = "Creating STAC-Metadata is finished!"
            logger.Logger(self.logger_properties)
        else:
            self.logger_properties["logger_level"] = "CRITICAL"
            self.logger_properties[
                "logger_msg"
            ] = "Creating STAC-Metadata is failed!"
            logger.Logger(self.logger_properties)
