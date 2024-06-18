# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

from typing import Union

from lxml import etree

from .. import logger, utils
from ..statics import constants
from . import recognizer


class NestedCollectionInspector(object):
    """
    This class will generate Collection IDs, Titles and
    their corresponding URLs for a presumed nested
    number originating from the Recognizer class
    in TDS. Only works for nested scenarios number 1,2,3,8
    and 9 in Recognizer class.
    The output will be a list of the tuples:
    (Root collection URL, Collection ID, Collection Title, corresponding subset URLs)

    Args:
        main_catalog_url (str): The URL of the TDS catalog
        nested_number (int, optional): Number of depth for nested datasets
        logger_properties (dict, optional): A dictionary for logger properties
        requests_properties (dict, optional): A dictionary for requests properties
    """

    main_catalog_url: str
    """
        The URL of the TDS catalog
    """
    nested_number: Union[int, None]
    """
        Number of depth for nested datasets
    """
    logger_properties: dict
    """
        A dictionary for logger properties. For more information see :class:`~tds2stac.logger.Logger`
    """
    requests_properties: dict
    """
        To obtain additional information on this topic, refer to
        the :class:`~tds2stac.TDS2STAC.requests_properties`. The default value is
        an empty dictionary.
    """

    def __init__(
        self,
        main_catalog_url: str,
        nested_number: Union[int, None] = None,
        logger_properties: dict = dict(),
        requests_properties: dict = dict(),
    ):
        self.requests_properties = requests_properties

        # using 'xml_processing' we get the XML contents of catalog URL.
        xml_url_catalog, id_catalog, xml = utils.xml_processing(
            main_catalog_url, self.requests_properties
        )
        if logger_properties is not None:
            self.logger_properties = logger_properties

        self.id_catalog = id_catalog
        self.xml_url_catalog = xml_url_catalog
        self.xml_url_catalog_temp = xml_url_catalog
        self.xml = xml
        self.all_urls: list = []
        self.corresponding_urls_ids: Union[list, None] = []
        self.depth_addresses: list = []

        self.nested_number = nested_number
        if self.nested_number is None:
            self.nested_number = 0
        if self.nested_number is not None:
            possible_nested_scenarios = [
                "First Scenario",
                "Third Scenario",
                "Second Scenario",
                "Eighth Scenario",
                "Ninth Scenario",
            ]

            if any(
                scenario
                in str(
                    recognizer.Recognizer(
                        main_catalog_url=self.xml_url_catalog,
                        requests_properties=self.requests_properties,
                    )
                )
                for scenario in possible_nested_scenarios
            ):
                if self.nested_number == 0:
                    # Getting the end point URLs of each dataset
                    self.final_collections_details_returner(
                        self.xml_url_catalog
                    )
                    # Finding the corresponding collection's URLs and IDs
                    collection_id = utils.replacement_func_collection_item_id(
                        xml_url_catalog
                    )
                    print(collection_id)
                    collection_title = utils.replacement_func(xml_url_catalog)
                    # Final variable than is a list of tuples and contains the
                    # corresponding collection's URLs and IDs and all related URLs
                    self.corresponding_urls_ids = [
                        (
                            xml_url_catalog,
                            collection_id,
                            collection_title,
                            self.all_urls,
                        )
                    ]
                else:
                    self.all_nested_dict: dict = {}
                    self.layer_dict: dict = {}
                    # Getting the list of all available datasets as a nested dictionary `self.all_nested_dict`
                    self.nested_dict_returner(
                        self.xml_url_catalog, self.all_nested_dict
                    )
                    # Getting the nested dictionary in a given depth `self.layer_dict`
                    self.layer_dict = self.n_level(
                        self.all_nested_dict, self.nested_number
                    )

                    # Getting the end point URLs of each dataset
                    # if isinstance(self.layer_dict, dict):
                    for i in self.layer_dict:
                        if isinstance(i, dict):
                            for k, v in i.items():
                                if isinstance(v, dict):
                                    self.end_point_url_extractor_dict(v)
                                if isinstance(v, list):
                                    self.end_point_url_extractor_list(v)
                                if isinstance(v, str):
                                    self.depth_addresses.append(v)
                        # rarely happens
                        if isinstance(i, list):
                            self.end_point_url_extractor_list(i)
                        if isinstance(i, str):
                            self.depth_addresses.append(i)

                    # Final variable than is a list of tuples and contains the
                    # corresponding collection's URLs and IDs and all related URLs
                    for i in self.depth_addresses:
                        self.all_urls = []
                        self.final_collections_details_returner(i)
                        collection_id = (
                            utils.replacement_func_collection_item_id(i)
                        )
                        collection_title = utils.replacement_func(i)
                        self.corresponding_urls_ids.append(
                            (i, collection_id, collection_title, self.all_urls)
                        )
                    if "Ninth Scenario" in str(
                        recognizer.Recognizer(
                            main_catalog_url=self.xml_url_catalog,
                            requests_properties=self.requests_properties,
                        )
                    ):
                        for i in self.corresponding_urls_ids:
                            for j in self.corresponding_urls_ids:
                                if i[0] in j[3]:
                                    j[3].remove(i[0])
            else:
                self.final_collections_details_returner(self.xml_url_catalog)
                # Finding the corresponding collection's URLs and IDs
                collection_id = utils.replacement_func_collection_item_id(
                    xml_url_catalog
                )
                print(collection_id)
                collection_title = utils.replacement_func(xml_url_catalog)
                # Final variable than is a list of tuples and contains the
                # corresponding collection's URLs and IDs and all related URLs
                self.corresponding_urls_ids = [
                    (
                        xml_url_catalog,
                        collection_id,
                        collection_title,
                        self.all_urls,
                    )
                ]
        self.logger_properties["logger_level"] = "INFO"
        self.logger_properties["logger_msg"] = self.corresponding_urls_ids
        logger.Logger(self.logger_properties)

    def end_point_url_extractor_dict(self, d: dict):
        """
        A function for extracting the end point URLs
        of a nested dictionary.

        Args:
            d (dict): A nested dictionary
        """
        for k, v in d.items():
            if isinstance(v, dict):
                # it should be v or d ?????
                self.end_point_url_extractor_dict(v)
            if isinstance(v, list):
                self.end_point_url_extractor_list(v)
            if isinstance(v, str):
                # if isinstance(self.depth_addresses, list):
                self.depth_addresses.append(v)

    def end_point_url_extractor_list(self, list_: list):
        """
        A function for extracting the end point URLs
        of a nested list.

        Args:
            list_ (list): A nested list
        """
        for i in list_:
            if isinstance(i, dict):
                self.end_point_url_extractor_dict(i)
            if isinstance(i, list):
                self.end_point_url_extractor_list(i)
            if isinstance(i, str):
                # if isinstance(self.depth_addresses, list):
                self.depth_addresses.append(i)

    def to_level(self, d: dict, layer: int):
        """
        A function for getting the a dictionary
        in a given depth. https://stackoverflow.com/a/68228562

        Args:
            d (dict): A nested dictionary
            layer (int): The depth of the dictionary

        """

        if layer:  # make sure level is not 0
            if not isinstance(d, (list, dict)):
                yield d  # not a dictionary or list, does not need to be traversed
            elif isinstance(d, dict):
                for (
                    a,
                    b,
                ) in (
                    d.items()
                ):  # element is a dictionary, have to transform it
                    if not (
                        n := list(self.to_level(b, layer - 1))
                    ):  # check this is the last level
                        yield a  # current level is `1`, so only yield back the key of the dictionary (no need to traverse the values, as we are out of depth)
                    else:  # at a level `l > 1`, so we need to transform the key's value
                        if isinstance(b, (str, list)) or (
                            len(b) == 1 and not isinstance(b, list)
                        ):
                            n = n[
                                0
                            ]  # original value `b` was a dictionary with a single key, a string, or a list
                        elif isinstance(b, dict) and all(
                            isinstance(i, dict) for i in n
                        ):
                            n = dict([j for k in n for j in k.items()])  # type: ignore  # `b` was a dictionary with more than one key, or a dictionary with multiple additional levels to traverse
                        yield {
                            a: n
                        }  # yield back the key and its transformed value as its own dictionary
            else:
                yield [
                    j for k in d for j in self.to_level(k, layer)
                ]  # value to transform is a list, simply map `to_level` to each element and yield the resulting list

    def n_level(self, d: dict, layer: int):
        """
        For decoding the generator object
        of `to_level` function. https://stackoverflow.com/a/68228562

        Args:
            d (dict): A nested dictionary
            layer (int): The depth of the dictionary
        """
        return list(self.to_level(d, layer))

    def nested_dict_returner(self, url: str, dict: dict):
        """
        A function for getting the nested dictionary
        of a given URL.

        Args:
            url (str): The URL of the TDS catalog
            dict (dict): A nested dictionary
        """

        xml_url_catalog, id_catalog, xml = utils.xml_processing(
            url, self.requests_properties
        )

        try:
            tree = etree.XML(xml)
        except BaseException:
            # self.logger.warning(
            #     "The Catalog is not reachable. Check the Catalg URL in the TDS"
            # )
            return (
                "The Catalog is not reachable. Check the Catalg URL in the TDS"
            )

        if tree.findall(".//{%s}catalogRef" % constants.unidata) != [] or (
            tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata) != []
            and tree.findall(".//{%s}catalogRef" % constants.unidata) != []
        ):
            for child in tree.findall(
                ".//{%s}catalogRef" % constants.unidata
            ) + tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata):
                if "catalogRef" in str(child):
                    # print(utils.references_urls(url, child.get("{%s}href" % constants.w3)))
                    dict[
                        utils.references_urls(
                            url, child.get("{%s}href" % constants.w3)
                        )
                    ] = {}
                    dic = dict[
                        utils.references_urls(
                            url, child.get("{%s}href" % constants.w3)
                        )
                    ]
                    self.nested_dict_returner(
                        utils.references_urls(
                            url, child.get("{%s}href" % constants.w3)
                        ),
                        dic,
                    )
                if (
                    "dataset" in str(child)
                    and len(
                        tree.findall(
                            ".//{%s}dataset[@urlPath]" % constants.unidata
                        )
                    )
                    == 1
                ):
                    dict[
                        url
                        + "?dataset="
                        + child.get("ID").replace("html", "xml")
                    ] = {}

                if (
                    "dataset" in str(child)
                    and len(
                        tree.findall(
                            ".//{%s}dataset[@urlPath]" % constants.unidata
                        )
                    )
                    > 1
                ):
                    dict[url.replace("html", "xml")] = {}

    def final_collections_details_returner(self, url: str):
        """
        A function for returning the URLs of input URL
        in First and Third cases in TDS

        Args:
            url (str): The URL of the TDS catalog
        """

        nested_scenarios = [
            "First Scenario",
            "Third Scenario",
            "Second Scenario",
            "Eighth Scenario",
            "Ninth Scenario",
        ]

        xml_url_catalog, id_catalog, xml = utils.xml_processing(
            url, self.requests_properties
        )

        try:
            tree = etree.XML(xml)
        except BaseException:
            # self.logger.warning(
            #     "The Catalog is not reachable. Check the Catalg URL in the TDS"
            # )
            return (
                "The Catalog is not reachable. Check the Catalg URL in the TDS"
            )

        if (
            tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata) == []
            and tree.findall(".//{%s}catalogRef" % constants.unidata) != []
        ):
            for child in tree.findall(".//{%s}catalogRef" % constants.unidata):
                if "catalogRef" in str(child):
                    self.final_collections_details_returner(
                        utils.references_urls(
                            url, child.get("{%s}href" % constants.w3)
                        )
                    )
                    recog = recognizer.Recognizer(
                        main_catalog_url=utils.references_urls(
                            url, child.get("{%s}href" % constants.w3)
                        ),
                        requests_properties=self.requests_properties,
                    )
                    if utils.references_urls(
                        url, child.get("{%s}href" % constants.w3)
                    ) not in self.all_urls and not any(
                        scenario in str(recog) for scenario in nested_scenarios
                    ):
                        self.all_urls.append(
                            utils.references_urls(
                                url, child.get("{%s}href" % constants.w3)
                            )
                        )
        if (
            tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata) != []
            and tree.findall(".//{%s}catalogRef" % constants.unidata) != []
        ):
            for child in tree.findall(
                ".//{%s}catalogRef" % constants.unidata
            ) + tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata):
                if "catalogRef" in str(child):
                    self.final_collections_details_returner(
                        utils.references_urls(
                            url, child.get("{%s}href" % constants.w3)
                        )
                    )
                    recog = recognizer.Recognizer(
                        main_catalog_url=utils.references_urls(
                            url, child.get("{%s}href" % constants.w3)
                        ),
                        requests_properties=self.requests_properties,
                    )
                    if utils.references_urls(
                        url, child.get("{%s}href" % constants.w3)
                    ) not in self.all_urls and not any(
                        scenario in str(recog) for scenario in nested_scenarios
                    ):
                        self.all_urls.append(
                            utils.references_urls(
                                url, child.get("{%s}href" % constants.w3)
                            )
                        )
                if (
                    "dataset" in str(child)
                    and len(
                        tree.findall(
                            ".//{%s}dataset[@urlPath]" % constants.unidata
                        )
                    )
                    == 1
                ):
                    if (
                        url
                        + "?dataset="
                        + child.get("ID").replace("html", "xml")
                        not in self.all_urls
                    ):
                        self.all_urls.append(
                            url
                            + "?dataset="
                            + child.get("ID").replace("html", "xml")
                        )
                if (
                    "dataset" in str(child)
                    and len(
                        tree.findall(
                            ".//{%s}dataset[@urlPath]" % constants.unidata
                        )
                    )
                    > 1
                ):
                    if url.replace("html", "xml") not in self.all_urls:
                        self.all_urls.append(url.replace("html", "xml"))
        if (
            tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata) != []
            and tree.findall(".//{%s}catalogRef" % constants.unidata) == []
        ):
            for child in tree.findall(".//{%s}catalogRef" % constants.unidata):
                self.all_urls = []

    def aslist(self):
        """
        A function for returning the list of tuples
        """
        return self.corresponding_urls_ids

    def __iter__(self):
        """
        A function for returning the iterator of tuples
        """
        return iter(self.aslist())
