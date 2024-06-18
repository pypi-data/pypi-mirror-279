# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
import sys
import traceback
from datetime import datetime
from typing import Union
from urllib.parse import quote_plus
from urllib.request import urlopen

import pytz
from dateutil.parser import parse
from lxml import etree

from . import logger, utils
from .analysers.recognizer import Recognizer
from .dimensions.spatial import Spatial
from .dimensions.temporal import Temporal
from .statics import constants
from .webservices import core


class CollectionHarvester(object):
    """
    This class harvests data pertaining to Collections
    from TDS catalogs. Depending on the sort of dataset
    scenario, it returns one of the five variables below.
    `collection_id` , `collection_title` , `collection_description`
    , `collection_url` , and `collection_subdirs`.

    Args:
        url (str): TDS catalog URL address
        recognizer (str): `status` scenario number of :class:`~tds2stac.Recognizer`
        subdirs (list): subdirs is a list of url, id, title, and subdirs of a nested dataset
        collection_tuples (list):  a tuple of STAC collection's auto-generated ID, user-ID, user-Title and user-Description defined by user.
        logger_properties (dict): dictionary of logger properties
        requests_properties (dict): dictionary of requests properties


    """

    url: str
    """
        TDS catalog URL address. Initial point of harvesting e.g.
        https://thredds.atmohub.kit.edu/thredds/catalog/caribic/IAGOS-CARIBIC_MS_files_collection_20231017/catalog.html (*)
    """
    recognizer: Union[str, None]
    """
        `status` scenario output of Recognizer class
    """
    subdirs: Union[list, None]
    """
        subdirs is a list of url, id, title, and subdirs of a nested dataset
    """
    collection_tuples: Union[list[tuple], None]
    """
        a tuple of STAC collection's auto-generated ID, user-ID, user-Title and user-Description defined by user.
    """
    logger_properties: dict
    """
        dictionary of logger properties, more information in :class:`~tds2stac.logger.Logger`
    """
    requests_properties: dict
    """
        To obtain additional information on this topic, refer to
        the :class:`~tds2stac.TDS2STAC.requests_properties`. The default value is
        an empty dictionary.
    """

    def __init__(
        self,
        url: str,
        recognizer: Union[str, None],
        subdirs: Union[list, None] = [],
        collection_tuples: Union[list[tuple], None] = None,
        logger_properties: dict = dict(),
        requests_properties: dict = dict(),
    ):
        ###############################################
        # Defining output and input variables as an empty parameter
        ###############################################
        self.collection_tuples = collection_tuples
        self.Recognizer_output = recognizer
        self.collection_id: Union[str, None] = None
        self.collection_title: Union[str, None] = None
        self.collection_description: Union[str, None] = None
        self.collection_url: Union[str, None] = None
        self.collection_subdirs: Union[list, None] = []
        if logger_properties is not None:
            self.logger_properties = logger_properties
        self.requests_properties = requests_properties
        ###############################################
        # Getting the Collection ID and Descriptionin
        # in none nested scenarios
        ###############################################
        if any(
            scenario in str(self.Recognizer_output)
            for scenario in constants.none_nested_scenarios
        ):
            (
                self.collection_id,
                self.collection_title,
                self.collection_description,
            ) = self.collection_id_desc_maker(
                url, self.collection_tuples, self.Recognizer_output
            )
            self.collection_url = url
        ###############################################
        # Getting the Collection ID and Descriptionin
        # in nested scenarios
        ###############################################
        if any(
            scenario in str(self.Recognizer_output)
            for scenario in constants.nested_scenarios
        ):
            #####################################
            # Collection cases with subdirs
            #####################################
            if subdirs is not None:
                if subdirs[3] != []:
                    self.collection_url = subdirs[0]
                    self.collection_id = subdirs[1]
                    self.collection_title = subdirs[2]
                    self.collection_subdirs = subdirs[3]
                    self.collection_description = (
                        "[Link to TDS](" + url.replace("xml", "html") + ")"
                    )
                    if self.collection_tuples is not None:
                        for i in self.collection_tuples:
                            if i[0] == self.collection_id:
                                if i[1] != "" and not i[1].isspace():
                                    self.collection_id = i[1]
                                else:
                                    self.collection_id = self.collection_id
                                if i[2] != "" and not i[2].isspace():
                                    self.collection_title = i[2]
                                else:
                                    self.collection_title = (
                                        self.collection_title
                                    )
                                if i[3] != "" and not i[3].isspace():
                                    if "[Link to TDS]" not in str(str(i[3])):
                                        self.collection_description = (
                                            str(i[3])
                                            .strip()
                                            .replace("\n", "\n\n")
                                            .replace('"', "")
                                            + "\n\n [Link to TDS]("
                                            + url.replace("xml", "html")
                                            + ")"
                                        )
                                    else:
                                        self.collection_description = (
                                            str(i[3])
                                            .strip()
                                            .replace("\n", "\n\n")
                                            .replace('"', "")
                                            + "  "
                                        )
                                else:
                                    self.collection_description = (
                                        self.collection_description
                                    )
                #####################################
                # Collection cases without subdirs
                #####################################
                else:
                    xml_url_catalog, id_catalog, xml = utils.xml_processing(
                        subdirs[0], self.requests_properties
                    )
                    recognizer_output_temp = Recognizer(
                        main_catalog_url=subdirs[0],
                        requests_properties=self.requests_properties,
                    )
                    self.collection_url = subdirs[0]
                    (
                        self.collection_id,
                        self.collection_title,
                        self.collection_description,
                    ) = self.collection_id_desc_maker(
                        url=xml_url_catalog,
                        collection_tuples=self.collection_tuples,
                        recognizer_output=recognizer_output_temp.status,
                    )

    def collection_id_desc_maker(
        self,
        url: str,
        collection_tuples: Union[list[tuple], None] = None,
        recognizer_output: Union[str, None] = None,
    ):
        """
        A function for getting collection id and description
        from the TDS catalog urls and pre-defined `collection_tuples`
        for scenarios number 4, 5, 6, 7 ,and 9

        Args:
            url (str): TDS catalog URL address
            collection_tuples (list):  a tuple of STAC collection's auto-generated ID, user-ID, user-Title and user-Description defined by user.
            recognizer_output (str): `status` scenario output of Recognizer class
        """

        if "Fourth Scenario" in str(recognizer_output):
            collection_id = utils.replacement_func_collection_item_id(
                url.replace("html", "xml")
            )

            collection_title = utils.replacement_func(
                url + " Empty".replace("html", "xml")
            )
            collection_description = (
                "[Link to TDS](" + url.replace("xml", "html") + ")"
            )

            if collection_tuples is not None:
                for i in collection_tuples:
                    if i[0] == collection_id:
                        if i[1] != "" and not i[1].isspace():
                            collection_id = i[1]
                        else:
                            collection_id = collection_id
                        if i[2] != "" and not i[2].isspace():
                            collection_title = i[2]
                        else:
                            collection_title = collection_title
                        if i[3] != "" and not i[3].isspace():
                            if "[Link to TDS]" not in str(i[3]):
                                collection_description = (
                                    str(i[3])
                                    .strip()
                                    .replace("\n", "\n\n")
                                    .replace('"', "")
                                    + "\n\n [Link to TDS]("
                                    + url.replace("xml", "html")
                                    + ")"
                                )
                            else:
                                collection_description = (
                                    str(i[3])
                                    .strip()
                                    .replace("\n", "\n\n")
                                    .replace('"', "")
                                    + "  "
                                )
                        else:
                            collection_description = collection_description
                        return (
                            collection_id,
                            collection_title,
                            collection_description,
                        )
            collection_id = utils.replacement_func_collection_item_id(
                url + "-empty".replace("html", "xml")
            )
            return collection_id, collection_title, collection_description
        fifth_and_ninth_scenarios = ["Fifth Scenario", "Ninth Scenario"]
        if any(x in str(recognizer_output) for x in fifth_and_ninth_scenarios):
            collection_id = utils.replacement_func_collection_item_id(
                url.replace("html", "xml")
            )

            collection_title = utils.replacement_func(
                url + " Collection".replace("html", "xml")
            )
            collection_description = (
                "[Link to TDS](" + url.replace("xml", "html") + ")"
            )

            if collection_tuples is not None:
                for i in collection_tuples:
                    if i[0] == collection_id:
                        if i[1] != "" and not i[1].isspace():
                            collection_id = i[1]
                        else:
                            collection_id = collection_id
                        if i[2] != "" and not i[2].isspace():
                            collection_title = i[2]
                        else:
                            collection_title = collection_title
                        if i[3] != "" and not i[3].isspace():
                            if "[Link to TDS]" not in str(i[3]):
                                collection_description = (
                                    str(i[3])
                                    .strip()
                                    .replace("\n", "\n\n")
                                    .replace('"', "")
                                    + "\n\n [Link to TDS]("
                                    + url.replace("xml", "html")
                                    + ")"
                                )
                            else:
                                collection_description = (
                                    str(i[3])
                                    .strip()
                                    .replace("\n", "\n\n")
                                    .replace('"', "")
                                    + "  "
                                )
                        else:
                            collection_description = collection_description
                        return (
                            collection_id,
                            collection_title,
                            collection_description,
                        )
            collection_id = utils.replacement_func_collection_item_id(
                url + "-collection".replace("html", "xml")
            )
            return collection_id, collection_title, collection_description

        if "Sixth Scenario" in str(recognizer_output):
            collection_id = utils.replacement_func_collection_item_id(
                url.replace("html", "xml")
            )
            collection_title = utils.replacement_func(
                url + " Single".replace("html", "xml")
            )
            collection_description = (
                "[Link to TDS](" + url.replace("xml", "html") + ")"
            )
            if collection_tuples is not None:
                for i in collection_tuples:
                    if i[0] == collection_id:
                        if i[1] != "" and not i[1].isspace():
                            collection_id = i[1]
                        else:
                            collection_id = collection_id
                        if i[2] != "" and not i[2].isspace():
                            collection_title = i[2]
                        else:
                            collection_title = collection_title
                        if i[3] != "" and not i[3].isspace():
                            if "[Link to TDS]" not in str(i[3]):
                                collection_description = (
                                    str(i[3])
                                    .strip()
                                    .replace("\n", "\n\n")
                                    .replace('"', "")
                                    + "\n\n [Link to TDS]("
                                    + url.replace("xml", "html")
                                    + ")"
                                )
                            else:
                                collection_description = (
                                    str(i[3])
                                    .strip()
                                    .replace("\n", "\n\n")
                                    .replace('"', "")
                                    + "  "
                                )
                        else:
                            collection_description = collection_description
                        return (
                            collection_id,
                            collection_title,
                            collection_description,
                        )
            collection_id = utils.replacement_func_collection_item_id(
                url + "-single".replace("html", "xml")
            )
            return collection_id, collection_title, collection_description

        if "Seventh Scenario" in str(recognizer_output):
            collection_id = utils.replacement_func_collection_item_id(
                url.replace("html", "xml")
            )
            collection_title = utils.replacement_func(
                url + " Aggregated".replace("html", "xml")
            )
            collection_description = (
                "[Link to TDS](" + url.replace("xml", "html") + ")"
            )
            if collection_tuples is not None:
                for i in collection_tuples:
                    if i[0] == collection_id:
                        if i[1] != "" and not i[1].isspace():
                            collection_id = i[1]
                        else:
                            collection_id = collection_id
                        if i[2] != "" and not i[2].isspace():
                            collection_title = i[2]
                        else:
                            collection_title = collection_title
                        if i[3] != "" and not i[3].isspace():
                            if "[Link to TDS]" not in str(i[3]):
                                collection_description = (
                                    str(i[3])
                                    .strip()
                                    .replace("\n", "\n\n")
                                    .replace('"', "")
                                    + "\n\n [Link to TDS]("
                                    + url.replace("xml", "html")
                                    + ")"
                                )
                            else:
                                collection_description = (
                                    str(i[3])
                                    .strip()
                                    .replace("\n", "\n\n")
                                    .replace('"', "")
                                    + "  "
                                )
                        else:
                            collection_description = collection_description
                        return (
                            collection_id,
                            collection_title,
                            collection_description,
                        )
            collection_id = utils.replacement_func_collection_item_id(
                url + "-aggregated".replace("html", "xml")
            )
            return collection_id, collection_title, collection_description

    def __iter__(self):
        yield "collection_id", self.collection_id
        yield "collection_title", self.collection_title
        yield "collection_description", self.collection_description
        yield "collection_url", self.collection_url
        yield "collection_subdirs", self.collection_subdirs


class ItemHarvester(object):
    """
    This class harvests information about an Item
    from TDS data catalogs. It ultimately returns
    a dictionary of harvesting variables, based on
    the type of dataset scenario and activated
    extensions.

    Args:
        url (str): TDS catalog URL address
        elem (str): xml element of the data in dataset
        harvesting_vars (dict): dictionary of harvesting variables that is going to be filled
        web_service_dict (dict): web service that the user wants to harvest from
        datetime_after (str): datetime that the user wants to harvest data after that
        datetime_before (str): datetime that the user wants to harvest data before that
        spatial_information (list): Spatial information of 2D datasets e.g. [minx, maxx, miny, maxy] or 1D dataset e.g. [x,y]
        temporal_format_by_dataname (str): datetime format for datasets that have datetime in their name e.g `e%y%m%d%H.%M%S%f`(optional),
        extension_properties (dict): dictionary of extension properties (optional)
        linestring (bool): using this attribute, user activate making LineString instead of Polygon (True and False)  (optional)
        logger_properties (dict): dictionary of logger properties
    """

    usl: str
    """
        TDS catalog URL address. Initial point of harvesting e.g.
        https://thredds.atmohub.kit.edu/thredds/catalog/caribic/IAGOS-CARIBIC_MS_files_collection_20231017/catalog.html (*)
    """
    elem: etree.Element
    """
        xml element of the data in dataset. It's an element of the
        xml file that is going to be harvested
    """
    harvesting_vars: dict
    """
        dictionary of harvesting variables that is going to be filled
    """
    web_service_dict: Union[dict, None]
    """
        web service that the user wants to harvest from
    """
    datetime_after: Union[str, None]
    """
        datetime that the user wants to harvest data after that
    """
    datetime_before: Union[str, None]
    """
        datetime that the user wants to harvest data before that
    """
    spatial_information: Union[list, None]
    """
        Spatial information of 2D datasets e.g. [minx, maxx, miny, maxy] or 1D dataset e.g. [x,y] (optional)
    """
    temporal_format_by_dataname: Union[str, None]
    """
        datetime format for datasets that have datetime in their name e.g `e%y%m%d%H.%M%S%f`(optional)
    """
    extension_properties: Union[dict, None]
    """
        dictionary of extension properties (optional)
    """
    linestring: bool
    """
        using this attribute, user activate making LineString instead of Polygon (True and False)  (optional)
    """
    requests_properties: dict
    """
        To obtain additional information on this topic, refer to
        the :class:`~tds2stac.TDS2STAC.requests_properties`. The default value is
        an empty dictionary.
    """
    logger_properties: dict
    """
        dictionary of logger properties, more information in :class:`~tds2stac.logger.Logger`
    """

    def __init__(
        self,
        url: str,
        elem: etree.Element,
        harvesting_vars: dict,
        web_service_dict: Union[dict, None],
        datetime_after: Union[datetime, None] = None,
        datetime_before: Union[datetime, None] = None,
        spatial_information: Union[list, None] = None,
        temporal_format_by_dataname: Union[str, None] = None,
        extension_properties: Union[dict, None] = None,
        linestring: bool = False,
        requests_properties: dict = dict(),
        logger_properties: dict = dict(),
    ):
        # Defining variables in TDS catalog and webservices as an empty parameter
        # Getting the item_id
        json_file_webservices: list = []
        self.harvesting_vars = harvesting_vars
        self.harvesting_vars["item_id"] = utils.replacement_func(
            elem.get("ID")
        )
        if logger_properties is not None:
            self.logger_properties = logger_properties
        if requests_properties is not None:
            self.requests_properties = requests_properties
        #################################
        # Opening the xml file
        #################################
        if "?dataset=" in url:
            data_get = utils.get_xml(
                url,
                self.requests_properties,
            )
        else:
            data_get = utils.get_xml(
                str(url) + "?dataset=" + str(elem.get("ID")),
                self.requests_properties,
            )

        #################################
        # Getting the tree of the xml file
        #################################
        try:
            tree_data = etree.XML(data_get)
        except etree.XMLSyntaxError:
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
            return
        else:
            try:
                ###############################################
                # It serves as a function to skip
                # data based on `datetime_before` and `datetime_after`
                ###############################################
                extracted_date = elem.find(
                    './/{%s}date[@type="modified"]' % constants.unidata
                )
                if extracted_date is not None:
                    try:
                        extracted_date = extracted_date.text
                        dt = parse(extracted_date)
                        self.harvesting_vars[
                            "modified_date_time"
                        ] = dt.replace(tzinfo=pytz.utc)
                    except ValueError:
                        ex_type, ex_value, ex_traceback = sys.exc_info()
                        if ex_type is not None and ex_value is not None:
                            self.logger_properties[
                                "logger_msg"
                            ] = "`datetime_filter` error: %s : %s" % (
                                ex_type.__name__,
                                ex_value,
                            )
                            self.logger_properties["logger_level"] = "ERROR"
                            logger.Logger(self.logger_properties)
                        return
                    else:
                        dt = dt.replace(tzinfo=pytz.utc)
                        if datetime_after and dt < datetime_after:
                            return
                        if datetime_before and dt > datetime_before:
                            return
                # bleedfixing datatime in STAC-Collection and STAC-Items for aggregated datasets. Should be fixed in the future
                else:
                    self.harvesting_vars["modified_date_time"] = parse(
                        datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fz")
                    ).replace(tzinfo=pytz.utc)
                    self.logger_properties[
                        "logger_msg"
                    ] = "The dataset does not have a modified datetime attribute so it is set to the current datetime"
                    self.logger_properties["logger_level"] = "INFO"
                    logger.Logger(self.logger_properties)
                ###############################################
                # Getting `dataset`, `catalog_url` and `catalog_id` of the data
                ###############################################
                self.harvesting_vars["dataset"] = tree_data.find(
                    "{%s}dataset" % constants.unidata
                )
                self.harvesting_vars["catalog_url"] = url.split("?")[0]
                self.harvesting_vars["main_dataset_url"] = url
                harvesting_vars["catalog_id"] = self.harvesting_vars[
                    "dataset"
                ].get("ID")
                metadata = self.harvesting_vars["dataset"].find(
                    "{%s}metadata" % constants.unidata
                )
                ########################################
                # Finding service tag in data tree element
                ########################################
                service_tag = self.harvesting_vars["dataset"].find(
                    "{%s}serviceName" % constants.unidata
                )
                if service_tag is None and metadata is not None:
                    service_tag = metadata.find(
                        "{%s}serviceName" % constants.unidata
                    )
                if service_tag is None:
                    # Use services found in the file depends on the version of TDS 4 or 5
                    try:
                        self.harvesting_vars["services"] = tree_data.findall(
                            ".//{%s}service[@serviceType='Compound']"
                            % constants.unidata
                        )
                        self.harvesting_vars["services_tuples"] = [
                            (s.get("base"), s.get("suffix"), s.get("name"))
                            for s in self.harvesting_vars["services"][0]
                        ]
                    except Exception:
                        self.harvesting_vars["services"] = tree_data.findall(
                            ".//{%s}service[@serviceType='compound']"
                            % constants.unidata
                        )
                        self.harvesting_vars["services_tuples"] = [
                            (s.get("base"), s.get("suffix"), s.get("name"))
                            for s in self.harvesting_vars["services"][0]
                        ]
                else:
                    # Use specific named services
                    self.harvesting_vars["services"] = tree_data.findall(
                        ".//{%s}service[@name='%s']"
                        % (constants.unidata, service_tag.text)
                    )
                    self.harvesting_vars["services_tuples"] = [
                        (s.get("base"), s.get("suffix"), s.get("name"))
                        for s in self.harvesting_vars["services"][0]
                    ]
                #############################################
                # Loop over all existing services in the data
                #############################################
                if "?dataset=" in url:
                    harvesting_vars["service_url_html"] = utils.xml2html(
                        str(url)
                    )
                else:
                    harvesting_vars["service_url_html"] = utils.xml2html(
                        str(url) + "?dataset=" + str(elem.get("ID"))
                    )
                if web_service_dict is not None:
                    if (
                        web_service_dict.get("web_service_config_file")
                        == "default"
                        or web_service_dict.get("web_service_config_file")
                        is None
                    ):
                        json_file = constants.default_tag_config_file
                    else:
                        json_file = web_service_dict["web_service_config_file"]
                scraper = core.JSONFileWebServiceListScraper(
                    json_file, self.logger_properties
                )
                json_file_webservices = scraper.load_and_process_json()
                extension_list = ["main_metadata"]

                if extension_properties is not None and isinstance(
                    extension_properties.get("item_extensions"), list
                ):
                    for item_extension in extension_properties[
                        "item_extensions"
                    ]:
                        if isinstance(item_extension, str):
                            extension_list.append(item_extension)
                        elif isinstance(item_extension, tuple):
                            extension_list.append(item_extension[0])
                if extension_properties is not None and isinstance(
                    extension_properties.get("collection_extensions"), list
                ):
                    for collection_extension in extension_properties[
                        "collection_extensions"
                    ]:
                        if isinstance(collection_extension, str):
                            extension_list.append(collection_extension)
                        elif isinstance(collection_extension, tuple):
                            extension_list.append(collection_extension[0])

                # if extension_properties is not None and extension_properties["item_common_metadata"] is True:
                #     extension_list.extend("common_metadata")
                # if extension_properties is not None and (extension_properties["item_scientific"] is True or extension_properties["collection_scientific"] is True):
                #     extension_list.extend("scientific_extension")

                for i, service in enumerate(self.harvesting_vars["services"]):
                    if (
                        service.get("serviceType") == "Compound"
                        or service.get("serviceType") == "compound"
                    ):
                        services_list = service.findall(
                            "{%s}service" % constants.unidata
                        )
                        services_list.append(url)

                        for s in services_list:
                            if (
                                s != url
                                and s.get("name") in json_file_webservices
                            ):
                                if s == url:
                                    s_get_name = "catalog"
                                    service_url = url
                                else:
                                    service_url = utils.references_urls(
                                        url, s.get("base")
                                    ) + self.harvesting_vars["dataset"].get(
                                        "urlPath"
                                    )

                                    s_get_name = s.get("name")
                                    if s.get("suffix") is not None:
                                        service_url += s.get("suffix")
                                    if s_get_name in ["iso", "ncml", "uddc"]:
                                        service_url += (
                                            "?dataset=%s&&catalog=%s"
                                            % (
                                                self.harvesting_vars[
                                                    "catalog_id"
                                                ],
                                                quote_plus(
                                                    self.harvesting_vars[
                                                        "catalog_url"
                                                    ]
                                                ),
                                            )
                                        )
                                    if s_get_name in ["wms"]:
                                        service_url += "?service=WMS&version=1.3.0&request=GetCapabilities"
                                    if s_get_name in ["dap4"]:
                                        service_url += ".dmr.xml"

                                if web_service_dict is not None and (
                                    web_service_dict.get("webservices")
                                    is not None
                                    and all(
                                        a.lower()
                                        in constants.supported_webservices
                                        for a in web_service_dict[
                                            "webservices"
                                        ]
                                    )
                                    and any(
                                        "/thredds/" + b.lower() + "/"
                                        in service_url
                                        for b in web_service_dict[
                                            "webservices"
                                        ]
                                    )
                                ):
                                    # To prevent 400 HTTP error
                                    try:
                                        if (
                                            self.requests_properties.get(
                                                "auth"
                                            )
                                            is not None
                                        ):
                                            utils.opener_module(
                                                service_url=service_url,
                                                requests_properties=self.requests_properties,
                                            )

                                        root = etree.XML(
                                            urlopen(service_url).read()
                                        )
                                        # root_nested = etree.parse(urlopen(service_url)).getroot()
                                    except Exception:
                                        (
                                            ex_type,
                                            ex_value,
                                            ex_traceback,
                                        ) = sys.exc_info()
                                        if (
                                            ex_type is not None
                                            and ex_value is not None
                                        ):
                                            self.logger_properties[
                                                "logger_msg"
                                            ] = (
                                                "400 HTTP verifier error code `urlopen`: %s: %s . It appears that the %s webservice you are utilizing in your configuration is deactivated or not working. Please check the `tag_config.json` file or ensure the web service is activated."
                                                % (
                                                    ex_type.__name__,
                                                    ex_value,
                                                    s_get_name,
                                                )
                                            )
                                            self.logger_properties[
                                                "logger_level"
                                            ] = "ERROR"
                                            logger.Logger(
                                                self.logger_properties
                                            )
                                        print(traceback.format_exc())
                                        continue

                                    core.WebServiceContentScraper(
                                        root,
                                        service_url,
                                        json_file,
                                        extension_list,
                                        harvesting_vars,
                                        self.logger_properties,
                                    )

                                elif web_service_dict is not None and (
                                    web_service_dict.get("webservices")
                                    is not None
                                    and not all(
                                        a.lower()
                                        in constants.supported_webservices
                                        for a in web_service_dict[
                                            "webservices"
                                        ]
                                    )
                                    and not any(
                                        "/thredds/" + b.lower() + "/"
                                        in service_url
                                        for b in web_service_dict[
                                            "webservices"
                                        ]
                                    )
                                ):
                                    self.logger_properties[
                                        "logger_msg"
                                    ] = "It couldn't find any activated web service according to your `tag_config.json` configuration. Please check your web service configuration file, `tag_config.json`"
                                    self.logger_properties[
                                        "logger_level"
                                    ] = "ERROR"
                                    logger.Logger(self.logger_properties)
                                    continue

                    spatial = Spatial()
                    spatial_output = spatial.regulator(
                        self.harvesting_vars, spatial_information
                    )
                    if isinstance(spatial_output, list):
                        spatial_output = list(dict.fromkeys(spatial_output))
                        for error in spatial_output:
                            self.logger_properties["logger_msg"] = error
                            self.logger_properties["logger_level"] = "ERROR"
                            logger.Logger(self.logger_properties)
                        # important break, because spatial infos is one of mandatory elements of STAC
                        continue
                    else:
                        (
                            self.harvesting_vars["horizontal_extent_lon_min"],
                            self.harvesting_vars["horizontal_extent_lon_max"],
                            self.harvesting_vars["horizontal_extent_lat_min"],
                            self.harvesting_vars["horizontal_extent_lat_max"],
                        ) = spatial_output

                        spatial.harvester(self.harvesting_vars, linestring)

                    #########################################
                    # Harvesting and then regulating temporal
                    # information from the data
                    #########################################

                    temporal_class = Temporal()
                    errors, warnings = temporal_class.regulator(
                        self.harvesting_vars,
                        temporal_format_by_dataname,
                        elem.get("name"),
                    )
                    if isinstance(errors, list):
                        errors = list(dict.fromkeys(errors))
                        for error in errors:
                            self.logger_properties["logger_msg"] = error
                            self.logger_properties["logger_level"] = "CRITICAL"
                            logger.Logger(self.logger_properties)
                        # important break, because temporal infos is one of mandatory elements of STAC
                        continue
                    if isinstance(warnings, list):
                        warnings = list(dict.fromkeys(warnings))
                        for warning in warnings:
                            self.logger_properties["logger_msg"] = warning
                            self.logger_properties["logger_level"] = "WARNING"
                            logger.Logger(self.logger_properties)

                    self.harvesting_vars["collection_interval_time_final"] = [
                        self.harvesting_vars["collection_interval_time"][0],
                        self.harvesting_vars["collection_interval_time"][-1],
                    ]

            except Exception:
                ex_type, ex_value, ex_traceback = sys.exc_info()
                if ex_type is not None and ex_value is not None:
                    self.logger_properties["logger_msg"] = (
                        "It couldn't make any items for the collections. Check your `tag_config.json` file. `ItemHarvester` error: %s : %s"
                        % (
                            ex_type.__name__,
                            ex_value,
                        )
                    )
                    self.logger_properties["logger_level"] = "CRITICAL"
                    logger.Logger(self.logger_properties)
                print(traceback.format_exc())
                return

    def __iter__(self):
        for key in self.harvesting_vars.keys():
            yield key, self.harvesting_vars[key]
