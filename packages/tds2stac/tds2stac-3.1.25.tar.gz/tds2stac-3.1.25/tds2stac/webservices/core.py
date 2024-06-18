# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0


import json

# import traceback
from typing import Any, List, Union

from lxml import etree

from .. import utils
from ..analysers.properties_verifier import Verifier
from ..logger import Logger
from ..statics import constants


class JSONFileWebServiceListScraper(object):
    """
    A class to get all `tds2stac_webservice_analyser` in tag_config.json
    file when `tds2stac_mode_analyser` is `get` or `check`.
    """

    def __init__(self, json_file: str, logger_properties: dict = dict()):
        self.json_file = json_file
        self.logger_properties = (
            logger_properties if logger_properties is not None else {}
        )

    def load_and_process_json(self):
        json_webservice_set = set()
        try:
            with open(self.json_file) as file:
                loaded_json = json.load(file)

            for key, value in loaded_json.items():
                if isinstance(value, dict):
                    for key1, value1 in value.items():
                        if isinstance(value1, dict):
                            tds2stac_mode = value1.get(
                                "tds2stac_mode_analyser"
                            )
                            if tds2stac_mode in ["get", "check"]:
                                json_webservice_set.add(
                                    value1.get("tds2stac_webservice_analyser")
                                )
                                break

            del loaded_json
        except Exception as e:
            self.logger_properties["logger_level"] = "CRITICAL"
            self.logger_properties[
                "logger_msg"
            ] = f"Failed to process file {self.json_file}: {str(e)}"
            Logger(self.logger_properties)

        return list(json_webservice_set)


class WebServiceListScraper(object):
    """
    A class for getting the list of available web services
    of a TDS catalogs.

        Args:
            url (str): The catalog URL from TDS to provide its web services
            logger_properties (dict, optional):The dictionary of the logger properties.
            requests_properties (dict, optional): A dictionary that modify the requests to URLs.
    """

    url: str
    """
    url is the url of the TDS catalog
    """
    logger_properties: dict
    """
    The dictionary of the logger properties. You can look at keys in :class:`~tds2stac.logger.Logger` class.
    """
    requests_properties: dict
    """
    To obtain additional information on this topic, refer to the :class:`~tds2stac.TDS2STAC.requests_properties`. The default value is an empty dictionary.
    """

    def __init__(
        self,
        url: str,
        logger_properties: dict = dict(),
        requests_properties: dict = dict(),
    ):
        ###############################################
        verifier = Verifier()
        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            verifier.logger_properties(logger_properties)
        if requests_properties is not None and isinstance(
            requests_properties, dict
        ):
            verifier.requests_properties(requests_properties)
        if logger_properties is not None and isinstance(
            logger_properties, dict
        ):
            self.logger_properties = logger_properties
        self.requests_properties = requests_properties
        self.logger_properties = logger_properties
        self.webserivces = []
        url_xml, id_xml, xml = utils.xml_processing(
            url, self.requests_properties
        )
        #################################
        # Getting the tree of the xml file
        #################################
        try:
            tree_data = etree.XML(xml)
        except Exception:
            self.logger_properties["logger_level"] = "CRITICAL"
            self.logger_properties[
                "logger_msg"
            ] = "The TDS Catalog URL does not provide any accessible services. Check it manually!"
            Logger(self.logger_properties)
            return
        else:
            try:
                ###############################################
                # Getting `dataset`, `catalog_url` and `catalog_id` of the data
                ###############################################
                dataset = tree_data.find("{%s}dataset" % constants.unidata)
                metadata = dataset.find("{%s}metadata" % constants.unidata)
                ########################################
                # Finding service tag in data tree element
                ########################################
                service_tag = dataset.find(
                    "{%s}serviceName" % constants.unidata
                )
                if service_tag is None and metadata is not None:
                    service_tag = metadata.find(
                        "{%s}serviceName" % constants.unidata
                    )
                if service_tag is None:
                    # Use services found in the file depends on the version of TDS 4 or 5
                    try:
                        services = tree_data.findall(
                            ".//{%s}service[@serviceType='Compound']"
                            % constants.unidata
                        )
                    except Exception:
                        services = tree_data.findall(
                            ".//{%s}service[@serviceType='compound']"
                            % constants.unidata
                        )
                else:
                    # Use specific named services
                    services = tree_data.findall(
                        ".//{%s}service[@name='%s']"
                        % (constants.unidata, service_tag.text)
                    )
                #############################################
                # Loop over all existing services in the data
                #############################################
                self.webserivces = [
                    s.get("name")
                    for i in services
                    for s in i.findall("{%s}service" % constants.unidata)
                    if (
                        i.get("serviceType") == "Compound"
                        or i.get("serviceType") == "compound"
                    )
                    # and s.get("name") in constants.supported_webservices
                ]
                self.webserivces = list(dict.fromkeys(self.webserivces))
            except Exception:
                self.logger_properties["logger_level"] = "CRITICAL"
                self.logger_properties[
                    "logger_msg"
                ] = "The TDS Catalog URL does not provide any accessible services!"
                Logger(self.logger_properties)
                # print(traceback.format_exc())
                return

    def aslist(self):
        return self.webserivces

    def __iter__(self):
        return iter(self.aslist())


class ConfigFileWebServicesScraper(object):
    """
    A class for getting the list of webservices that used
    in the `tag_config.json` file.
    Args:
        json_file (str): The path to the `tag_config.json` file
        logger_properties (dict): The dictionary of the logger properties.
    """

    json_file: str
    """
    The path to the `tag_config.json` file.To obtain further details on the creation of a
    `tag_config.json` file, refer: :ref:`tag-config`.
    """
    logger_properties: dict
    """
    The dictionary of the logger properties. You can look at keys in :class:`~tds2stac.logger.Logger` class.
    """

    def __init__(self, json_file: str, logger_properties: dict = dict()):
        self.json_file = json_file
        self.logger_properties = logger_properties
        self.values: list = []
        loaded_json = json.load(open(json_file))
        self.get_values(loaded_json, "tds2stac_webservice_analyser")

    def get_values(self, json_obj: Union[dict, list], key: str):
        """
        A function for getting the list of values of a
        specific key in a json file.
        """
        if isinstance(json_obj, dict):
            for k, v in json_obj.items():
                if k == key:
                    self.values.append(v)
                if isinstance(v, (dict, list)):
                    self.get_values(v, key)
        elif isinstance(json_obj, list):
            for item in json_obj:
                self.get_values(item, key)
        else:
            self.logger_properties["logger_level"] = "CRITICAL"
            self.logger_properties[
                "logger_msg"
            ] = f"The json file is not in a right format. Check the following file: {self.json_file}"
            Logger(self.logger_properties)

        return self.values

    def aslist(self):
        """
        A function for returning the list of webservices
        """
        self.values = list(dict.fromkeys(self.values))
        return self.values

    def __iter__(self):
        """
        A function for returning the iterator of webservices
        """
        return iter(self.aslist())


class WebServiceContentScraper(object):
    """
    The functionality of the existing class is dependent on the settings
    specified in the `tag_config.json` file in order to harvest targeted
    information from a selected web service. For comprehensive instructions
    on configuring the `tag_config.json` file, refer to the following link:
    :ref:`tag-config`.

        Args:
            root (etree._Element): The root of the XML-based web service
            json_file (str): The path to the `tag_config.json` file
            extensions_list (list): The list of extensions to be harvested
                from the web service (main keys in the `tag_config.json` file)
            harvesting_vars (dict, optional): The dictionary of harvesting variables
            logger_properties (dict, optional):The dictionary of the logger properties.
    """

    root: etree._Element
    """
    Etree root object of the XML-based web service
    """
    json_file: str
    """
    The path to the `tag_config.json` file
    """
    extensions_list: list
    """
    The list of extensions to be harvested from the web service.
    Main keys in the `tag_config.json` file. For example `item_datacube_extension`
    and so on.
    """
    harvesting_vars: Union[dict, None]
    """
    It's a dictionary that keys are variable names and values are the result of harvesting.
    """
    logger_properties: dict
    """
    The dictionary of the logger properties. You can look at keys in :class:`~tds2stac.logger.Logger` class.
    """

    def __init__(
        self,
        root: etree._Element,
        service_url: str,
        json_file: str,
        extensions_list: list,
        harvesting_vars: Union[dict, None] = None,
        logger_properties: dict = dict(),
    ):
        self.logger_properties = logger_properties
        tag_config_json = json.load(open(json_file))
        self.list_of_all_tags: List[Any] = []
        for extension in extensions_list:
            self.harvester(
                root, service_url, tag_config_json, extension, harvesting_vars
            )
        del tag_config_json

    def harvester(
        self, root, service_url, json_file, ext_name, harvesting_vars=None
    ):
        for k, v in json_file[ext_name].items():
            xpath_string_schema = ""
            namespaces_ = dict()
            action_type = []
            values_with_none_ = []
            list_of_all_tags_with_none = []
            if v is not None and isinstance(v, dict):
                # Main function starts from this point. because it finds the attrs of a tag
                if v.get("tds2stac_mode_analyser") == "str":
                    harvesting_vars[k] = v.get("tds2stac_manual_variable")
                    if harvesting_vars[k] is None:
                        self.logger_properties["logger_level"] = "WARNING"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"The '{k}' is empty or in a wrong format. Check '{k}' key in your `tag_config.json` file."
                        Logger(self.logger_properties)
                elif v.get("tds2stac_mode_analyser") == "list":
                    Logger(self.logger_properties)
                    if v.get("tds2stac_manual_variable") is not None:
                        harvesting_vars[k] = (
                            v.get("tds2stac_manual_variable")
                            .strip("][")
                            .split(", ")
                        )
                    else:
                        self.logger_properties["logger_level"] = "WARNING"
                        self.logger_properties[
                            "logger_msg"
                        ] = f"The '{k}' is empty or in a wrong format. Check '{k}' key in your `tag_config.json` file."
                elif v.get("tds2stac_mode_analyser") == "get":
                    if v.get("tds2stac_webservice_analyser") is not None:
                        if (
                            f"/thredds/{v.get('tds2stac_webservice_analyser')}/"
                            in service_url
                        ):
                            # make a function to make a string to input to the xpath function
                            if v.get("tds2stac_reference_key") is not None:
                                self.logger_properties[
                                    "logger_level"
                                ] = "WARNING"
                                self.logger_properties[
                                    "logger_msg"
                                ] = f"key '{k}': Using `tds2stac_reference_key` is not recommended. It would be better better to use `tds2stac_webservice_analyser` instead."
                                Logger(self.logger_properties)
                                for k1, v1 in v.items():
                                    if (
                                        k
                                        not in constants.static_list_webservices
                                    ):
                                        # A condition specifically for ISO 19115-2 XML files

                                        if isinstance(v1, dict):
                                            # This condition is for finding which method should
                                            # be used to get the result data. For example, if
                                            # all attributed were field, it means we should use
                                            # `tag.text` method to get the result data. If one of
                                            # the attributes were None, it means we should use
                                            # tag.get(attr) method to get the result data.
                                            if v1 == list(v.values())[-1]:
                                                if (
                                                    list(v1.values()).count(
                                                        None
                                                    )
                                                    == 0
                                                ):
                                                    values_with_none_.append(
                                                        "text_of_tag"
                                                    )
                                                    action_type.append(
                                                        "text_of_tag"
                                                    )
                                                elif (
                                                    list(v1.values()).count(
                                                        None
                                                    )
                                                    == 1
                                                ):
                                                    values_with_none_.extend(
                                                        list(v1.values())
                                                    )
                                                    action_type.append(
                                                        list(v1.keys())[
                                                            list(
                                                                v1.values()
                                                            ).index(None)
                                                        ]
                                                    )
                                                elif (
                                                    list(v1.values()).count(
                                                        None
                                                    )
                                                    > 1
                                                ):
                                                    list_of_more_than_one_None = [
                                                        v
                                                        for i, v in enumerate(
                                                            list(v1.values())
                                                        )
                                                        if v is None
                                                    ]
                                                    values_with_none_.extend(
                                                        list_of_more_than_one_None
                                                    )
                                                    list_of_more_than_one_None = [
                                                        list(v1.keys())[i]
                                                        for i, v in enumerate(
                                                            list(v1.values())
                                                        )
                                                        if v is None
                                                    ]
                                                    action_type.extend(
                                                        list_of_more_than_one_None
                                                    )

                                k_ref = v["tds2stac_reference_key"]
                                v_ref = json_file[ext_name][
                                    v["tds2stac_reference_key"]
                                ]
                                for k1, v1 in v_ref.items():
                                    if (
                                        k_ref
                                        not in constants.static_list_webservices
                                    ):
                                        # A condition specifically for ISO 19115-2 XML files
                                        if ":" in k1:
                                            schema = k1.split(":")[0]
                                            localname = k1.split(":")[1]
                                        else:
                                            schema = v_ref[
                                                "tds2stac_webservice_analyser"
                                            ]
                                            localname = k1
                                        # In this condition we don't add any attribute to the xpath string
                                        if v1 is None:
                                            xpath_string_schema += "/%s:%s" % (
                                                schema,
                                                localname,
                                            )
                                            namespaces_[
                                                schema
                                            ] = constants.schemas_dicts[schema]
                                        elif isinstance(v1, dict):
                                            # This condition is for finding which method should
                                            # be used to get the result data. For example, if
                                            # all attributed were field, it means we should use
                                            # tag.text method to get the result data. If one of
                                            # the attributes were None, it means we should use
                                            # tag.get(attr) method to get the result data.

                                            attribute_str = ""  # defining an empty string for collecting all tag elements and attributes for xpath search in the following loop
                                            for k2, v2 in v1.items():
                                                if v2 is not None:
                                                    attribute_str += (
                                                        '[@%s="%s"]'
                                                        % (
                                                            k2,
                                                            v2,
                                                        )
                                                    )
                                                # this condition defined for times that we have need to get one of the attributes of a tag
                                                elif (
                                                    v2 is None
                                                    and list(
                                                        v1.values()
                                                    ).count(None)
                                                    == 1
                                                ):
                                                    attribute_str += (
                                                        "[@%s]" % (k2)
                                                    )
                                                # For this condition we have to trigger (because it's within a loop
                                                # and might issue more than one log) a warning to inform the user that he/she
                                                #  should choose one of the attributes of a tag to restrict the search to the desirable tag attribute
                                                #  otherwise it will return a nested list.of elements that each list in the nested list
                                                #  is content of getting attribute of a tag.
                                                # For example if we define like {'name': null, 'value': null} it will return a nested list
                                                # like  [[... ,... ], [... ,... ]].
                                                elif (
                                                    v2 is None
                                                    and list(
                                                        v1.values()
                                                    ).count(None)
                                                    > 1
                                                ):
                                                    attribute_str += (
                                                        "[@%s]" % (k2)
                                                    )
                                                    self.logger_properties[
                                                        "logger_level"
                                                    ] = "WARNING"
                                                    self.logger_properties[
                                                        "logger_msg"
                                                    ] = f"It contains more than one null in the nested dict of '{k}'. You have to choose one of them. Revise your `tag_config.json` file."
                                                    Logger(
                                                        self.logger_properties
                                                    )

                                            xpath_string_schema += (
                                                "/%s:%s%s"
                                                % (
                                                    schema,
                                                    localname,
                                                    attribute_str,
                                                )
                                            )
                                            namespaces_[
                                                schema
                                            ] = constants.schemas_dicts[schema]

                                if namespaces_ != {}:
                                    self.list_of_all_tags = root.xpath(
                                        xpath_string_schema,
                                        namespaces=namespaces_,
                                    )
                                    if self.list_of_all_tags != []:
                                        for a in self.list_of_all_tags:
                                            if a.xpath(".//*") != []:
                                                list_of_all_tags_with_none_temp = (
                                                    []
                                                )
                                                for xx in a.xpath(".//*"):
                                                    if (
                                                        values_with_none_[0]
                                                        in xx.attrib.values()
                                                    ):
                                                        list_of_all_tags_with_none_temp.append(
                                                            xx
                                                        )
                                                    else:
                                                        # self.logger_properties[
                                                        #     "logger_level"
                                                        # ] = "ERROR"
                                                        # self.logger_properties[
                                                        #     "logger_msg"
                                                        # ] = f"The `tds2stac_reference_key` of '{k}' key is not valid. Check the `tag_config.json` file."
                                                        # Logger(self.logger_properties)
                                                        continue
                                                list_of_all_tags_with_none.extend(
                                                    list_of_all_tags_with_none_temp
                                                )
                                                if (
                                                    list_of_all_tags_with_none_temp
                                                    == []
                                                ):
                                                    list_of_all_tags_with_none.append(
                                                        None
                                                    )
                                            else:
                                                list_of_all_tags_with_none.append(
                                                    None
                                                )

                                    if len(list_of_all_tags_with_none) == 0:
                                        # self.logger_properties[
                                        #     "logger_level"
                                        # ] = "WARNING"
                                        # self.logger_properties[
                                        #     "logger_msg"
                                        # ] = f"It couldn't find any tag for the considered tag element '{k}'. It means you should check the tag element name in the `tag_config.json` file."
                                        # Logger(self.logger_properties)
                                        continue
                                    elif (
                                        len(list_of_all_tags_with_none) == 1
                                        and action_type != []
                                    ):
                                        if action_type[0] == "text_of_tag":
                                            harvesting_vars[
                                                k
                                            ] = list_of_all_tags_with_none[
                                                0
                                            ].text
                                        else:
                                            harvesting_vars[
                                                k
                                            ] = list_of_all_tags_with_none[
                                                0
                                            ].get(
                                                action_type[0]
                                            )
                                    elif len(list_of_all_tags_with_none) > 1:
                                        if action_type[0] == "text_of_tag":
                                            harvesting_vars[k] = [
                                                a.text
                                                if a is not None
                                                else None
                                                for a in list_of_all_tags_with_none
                                            ]
                                        else:
                                            harvesting_vars[k] = [
                                                a.get(action_type[b])
                                                if a is not None
                                                else None
                                                for b in range(
                                                    len(action_type)
                                                )
                                                for a in list_of_all_tags_with_none
                                            ]
                            else:
                                for k1, v1 in v.items():
                                    if (
                                        k
                                        not in constants.static_list_webservices
                                    ):
                                        # A condition specifically for ISO 19115-2 XML files
                                        if ":" in k1:
                                            schema = k1.split(":")[0]
                                            localname = k1.split(":")[1]
                                        else:
                                            schema = v.get(
                                                "tds2stac_webservice_analyser"
                                            )
                                            localname = k1
                                        # In this condition we don't add any attribute to the xpath string
                                        if v1 is None:
                                            xpath_string_schema += "/%s:%s" % (
                                                schema,
                                                localname,
                                            )
                                            if schema is not None:
                                                namespaces_[
                                                    schema
                                                ] = constants.schemas_dicts[
                                                    schema
                                                ]
                                            else:
                                                self.logger_properties[
                                                    "logger_level"
                                                ] = "WARNING"
                                                self.logger_properties[
                                                    "logger_msg"
                                                ] = f"`tds2stac_webservice_analyser` of '{k}' key is None. Revise your `tag_config.json` file."
                                                Logger(self.logger_properties)
                                                return
                                        elif isinstance(v1, dict):
                                            # This condition is for finding which method should
                                            # be used to get the result data. For example, if
                                            # all attributed were field, it means we should use
                                            # tag.text method to get the result data. If one of
                                            # the attributes were None, it means we should use
                                            # tag.get(attr) method to get the result data.
                                            if v1 == list(v.values())[-1]:
                                                if (
                                                    list(v1.values()).count(
                                                        None
                                                    )
                                                    == 0
                                                ):
                                                    action_type.append(
                                                        "text_of_tag"
                                                    )
                                                elif (
                                                    list(v1.values()).count(
                                                        None
                                                    )
                                                    == 1
                                                ):
                                                    action_type.append(
                                                        list(v1.keys())[
                                                            list(
                                                                v1.values()
                                                            ).index(None)
                                                        ]
                                                    )
                                                elif (
                                                    list(v1.values()).count(
                                                        None
                                                    )
                                                    > 1
                                                ):
                                                    list_of_more_than_one_None = [
                                                        list(v1.keys())[i]
                                                        for i, v in enumerate(
                                                            list(v1.values())
                                                        )
                                                        if v is None
                                                    ]
                                                    action_type.extend(
                                                        list_of_more_than_one_None
                                                    )
                                            attribute_str = ""  # defining an empty string for collecting all tag elements and attributes for xpath search in the following loop
                                            for k2, v2 in v1.items():
                                                if v2 is not None:
                                                    attribute_str += (
                                                        '[@%s="%s"]'
                                                        % (
                                                            k2,
                                                            v2,
                                                        )
                                                    )
                                                # this condition defined for times that we have need to get one of the attributes of a tag
                                                elif (
                                                    v2 is None
                                                    and list(
                                                        v1.values()
                                                    ).count(None)
                                                    == 1
                                                ):
                                                    attribute_str += (
                                                        "[@%s]" % (k2)
                                                    )
                                                # For this condition we have to trigger (because it's within a loop
                                                # and might issue more than one log) a warning to inform the user that he/she
                                                #  should choose one of the attributes of a tag to restrict the search to the desirable tag attribute
                                                #  otherwise it will return a nested list.of elements that each list in the nested list
                                                #  is content of getting attribute of a tag.
                                                # For example if we define like {'name': null, 'value': null} it will return a nested list
                                                # like  [[... ,... ], [... ,... ]].
                                                elif (
                                                    v2 is None
                                                    and list(
                                                        v1.values()
                                                    ).count(None)
                                                    > 1
                                                ):
                                                    # we have to define a Logger for this warning

                                                    attribute_str += (
                                                        "[@%s]" % (k2)
                                                    )
                                                    self.logger_properties[
                                                        "logger_level"
                                                    ] = "WARNING"
                                                    self.logger_properties[
                                                        "logger_msg"
                                                    ] = f"It contains more than one null in the nested dict of '{k}' and you have to choose one of them. Revise your `tag_config.json` file."
                                                    Logger(
                                                        self.logger_properties
                                                    )
                                            xpath_string_schema += (
                                                "/%s:%s%s"
                                                % (
                                                    schema,
                                                    localname,
                                                    attribute_str,
                                                )
                                            )
                                            namespaces_[
                                                schema
                                            ] = constants.schemas_dicts[schema]

                                if namespaces_ != {}:
                                    self.list_of_all_tags = root.xpath(
                                        xpath_string_schema,
                                        namespaces=namespaces_,
                                    )
                                    if len(self.list_of_all_tags) == 0:
                                        # self.logger_properties[
                                        #     "logger_level"
                                        # ] = "ERROR"
                                        # self.logger_properties[
                                        #     "logger_msg"
                                        # ] = f"It couldn't find any tag for the considered tag element '{k}'. It means you should check the tag element name in the `tag_config.json` file."
                                        # Logger(self.logger_properties)
                                        continue
                                    elif (
                                        len(self.list_of_all_tags) == 1
                                        and action_type != []
                                    ):
                                        if action_type[0] == "text_of_tag":
                                            harvesting_vars[
                                                k
                                            ] = self.list_of_all_tags[0].text
                                        else:
                                            harvesting_vars[
                                                k
                                            ] = self.list_of_all_tags[0].get(
                                                action_type[0]
                                            )
                                    elif len(self.list_of_all_tags) > 1:
                                        if action_type[0] == "text_of_tag":
                                            harvesting_vars[k] = [
                                                a.text
                                                for a in self.list_of_all_tags
                                            ]
                                        else:
                                            harvesting_vars[k] = [
                                                a.get(action_type[b])
                                                for b in range(
                                                    len(action_type)
                                                )
                                                for a in self.list_of_all_tags
                                            ]
                elif v.get("tds2stac_mode_analyser") == "check":
                    if v.get("tds2stac_webservice_analyser") is not None:
                        if (
                            f"/thredds/{v.get('tds2stac_webservice_analyser')}/"
                            in service_url
                        ):
                            # make a function to make a string to input to the xpath function
                            for k1, v1 in v.items():
                                if k not in constants.static_list_webservices:
                                    if ":" in k1:
                                        schema = k1.split(":")[0]
                                        localname = k1.split(":")[1]
                                    else:
                                        schema = v[
                                            "tds2stac_webservice_analyser"
                                        ]
                                        localname = k1
                                    if v1 is None:
                                        xpath_string_schema += "/%s:%s" % (
                                            schema,
                                            localname,
                                        )
                                        namespaces_[
                                            schema
                                        ] = constants.schemas_dicts[schema]
                                    elif isinstance(v1, dict):
                                        attribute_str = ""
                                        for k2, v2 in v1.items():
                                            if v2 is not None:
                                                attribute_str += (
                                                    '[@%s="%s"]'
                                                    % (
                                                        k2,
                                                        v2,
                                                    )
                                                )
                                            elif (
                                                v2 is None
                                                and list(v1.values()).count(
                                                    None
                                                )
                                                == 1
                                            ):
                                                attribute_str += "[@%s]" % (k2)
                                            elif (
                                                v2 is None
                                                and v1.values().count(None) > 1
                                            ):
                                                attribute_str += "[@%s]" % (k2)
                                                self.logger_properties[
                                                    "logger_level"
                                                ] = "WARNING"
                                                self.logger_properties[
                                                    "logger_msg"
                                                ] = f"It contains more than one null in the nested dict of '{k}' and you have to choose one of them. Revise your `tag_config.json` file."
                                                Logger(self.logger_properties)

                                        xpath_string_schema += "/%s:%s%s" % (
                                            schema,
                                            localname,
                                            attribute_str,
                                        )
                                        namespaces_[
                                            schema
                                        ] = constants.schemas_dicts[schema]
                            if namespaces_ != {}:
                                self.list_of_all_tags = root.xpath(
                                    xpath_string_schema, namespaces=namespaces_
                                )
                                if len(self.list_of_all_tags) == 0:
                                    # self.logger_properties["logger_level"] = "WARNING"
                                    # self.logger_properties[
                                    #     "logger_msg"
                                    # ] = f"It couldn't find any tag for the considered tag element '{k}'. It means you should check the tag element name in the `tag_config.json` file."
                                    # Logger(self.logger_properties)
                                    continue

                                elif len(self.list_of_all_tags) >= 1:
                                    harvesting_vars[k] = v[
                                        "tds2stac_manual_variable"
                                    ]
                elif v.get("tds2stac_mode_analyser") is None:
                    self.logger_properties["logger_level"] = "WARNING"
                    self.logger_properties[
                        "logger_msg"
                    ] = f"The 'tds2stac_mode_analyser' of '{k}' is None. Revise your `tag_config.json` file."
                    Logger(self.logger_properties)
