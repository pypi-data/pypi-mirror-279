# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

from typing import Union

import requests
from lxml import etree

from .. import logger, utils
from ..statics import constants


class Recognizer(object):
    """
    A class for recognizing nine different
    and possible scenarios in management of
    TDS datasets. We will explain each scenario
    in the following.

        First scenario: Just `catalogRef` tags are located directly under the dataset element tag.
            tag `https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/era5/sfc/single/catalog.xml` (nested)
        Second senarion: `CatalogRefs` are not under a dataset element tag and directly come below the `catalog`.
            `https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/sensor_catalog_ext.xml` (nested)
        Third scenario: One single `dataset` tag is located next to `CatalogRef` tags. All are under a `dataset` tag.
            `https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/catalog.xml` (nested)
        Fourth scenario: An empty datasets.
            `https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/bio_geo_chem_catalog_ext.xml` or `https://thredds.atmohub.kit.edu/thredds/catalog/snowfogs/catalog.xml`
        Fifth scenario: There is no `CatalogRef` tag and all are `dataset` tag. All of them are under a `dataset` tag.
            `https://thredds.imk-ifu.kit.edu/thredds/catalog/climate/raster/global/chelsa/v1.2/catalog.html`
        Sixth scenario: A single dataset
            `https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/era5/sfc/single/catalog.xml?dataset=regclim/raster/global/era5/sfc/single/era5_sfc_20210101.nc`
        Seventh scenario: An aggregated dataset
            `https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/swabian_moses_2021.xml?dataset=swabian_moses_aggregation`
        Eighth scenario: A combination of `caralogRef` and `dataset` tags that is not under a `dataset` tag.It's similar to second scenario but with datasets
            `https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/transfer.xml`
        Ninth scenario: When we have a bunch of single `dataset` tags next to catalogref. It's similar to third scenario but with more datasets.
            `https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/hydrogfd/v3.0/catalog.xml` (nested)



    Args:
        main_catalog_url: TDS Catalog url to start harvesting
        nested_check: An option for checking nested datasets in TDS (True or False)
        auth: Authentication for TDS catalog e.g.('user', 'password')
        logger_properties: A dictionary for logger properties.
        requests_properties: A dictionary for requests properties.
    """

    main_catalog_url: str
    """
        TDS Catalog url to start harvesting (*)
    """
    nested_check: bool
    """
        An option for checking nested datasets in TDS (True or False) (optional)
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
        nested_check: bool = False,
        logger_properties: dict = dict(),
        requests_properties: dict = dict(),
    ):
        if logger_properties is not None:
            self.logger_properties = logger_properties
        self.requests_properties = requests_properties
        self.all_dirs: list = []
        self.all_href: list = []
        self.all_dirs_extensions: list = []
        self.nested_check = nested_check
        self.nested_num: int = 0
        self.nested_num_temp: int = 0
        self.status: Union[str, None] = None

        # using 'xml_processing' we get the XML contents of catalog URL.
        xml_url_catalog, id_catalog, xml = utils.xml_processing(
            main_catalog_url, self.requests_properties
        )

        self.id_catalog = id_catalog
        self.xml_url_catalog = xml_url_catalog
        self.xml_url_catalog_temp = xml_url_catalog
        self.xml = xml
        self.recognition_function(self.xml_url_catalog, self.xml)
        self.logger_properties["logger_level"] = "INFO"
        self.logger_properties[
            "logger_msg"
        ] = f"{self.status, self.nested_num}"
        logger.Logger(self.logger_properties)

    def recognition_function(self, url: str, xml_content):
        """
        A function for recognizing number of scenarios
        in TDS
        """

        # Opening the Catalog url
        try:
            tree = etree.XML(xml_content)
            # return [e for e in tree]
        except BaseException:
            return (
                "The Catalog is not reachable. Check the Catalg URL in the TDS"
            )

        # we have nine different cases.
        # First, catalogRefs are under the dataset tag (https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/era5/sfc/single/catalog.html) --> nested
        # and one without dataset tag directly with catalogRef(https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/sensor_catalog_ext.html) --> nested
        # the third one is the case that we have a single data next to catalogRefs (https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/catalog.html) --> nested
        # the fourth is empty datasets (https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/bio_geo_chem_catalog_ext.html or https://thredds.atmohub.kit.edu/thredds/catalog/snowfogs/catalog.html)
        # the fifth one is having all data under the dataset (https://thredds.imk-ifu.kit.edu/thredds/catalog/climate/raster/global/chelsa/v1.2/catalog.html)
        # the sixth one is a single data (https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/era5/sfc/single/catalog.html?dataset=regclim/raster/global/era5/sfc/single/era5_sfc_20210101.nc)
        # the seventh is a aggregated data (https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/swabian_moses_2021.html?dataset=swabian_moses_aggregation)
        # the eighth case is combination of caralogRef and dataset that is not under a dataset tag like second case but with dataset (https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/transfer.html)
        # the ninth case is the case when we have a bunch of single data next to catalogref (https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/hydrogfd/v3.0/catalog.html) --> nested

        all_tags_list = [e for e in tree]

        if "catalogRef" not in str(all_tags_list) and "dataset" in str(
            all_tags_list
        ):
            # First and third to seventh cases are here
            # First case:
            if (
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
                == []
                and tree.findall(".//{%s}catalogRef" % constants.unidata) != []
            ):
                if self.nested_check is not True:
                    self.status = "First Scenario"
                    return self.status
                else:
                    self.nested_num = 0
                    self.nested_num_temp = 0
                    self.nested_checker(url)

                    for i in self.all_dirs:
                        if i.count("/") > self.nested_num:
                            self.nested_num = i.count("/")
                    self.nested_num = self.nested_num + 1
                    self.status = "First Scenario"
                    return self.status, self.nested_num
            # Third case:
            if (
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
                != []
                and len(
                    tree.findall(
                        ".//{%s}dataset[@urlPath]" % constants.unidata
                    )
                )
                == 1
                and tree.findall(".//{%s}catalogRef" % constants.unidata) != []
            ):
                if self.nested_check is not True:
                    self.status = "Third Scenario"
                    return self.status
                else:
                    self.nested_num = 0
                    self.nested_num_temp = 0
                    self.nested_checker(url)

                    for i in self.all_dirs:
                        if i.count("/") > self.nested_num:
                            self.nested_num = i.count("/")
                    self.nested_num = self.nested_num + 1
                    self.status = "Third Scenario"
                    return self.status, self.nested_num

            # Ninth case:
            if (
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
                != []
                and len(
                    tree.findall(
                        ".//{%s}dataset[@urlPath]" % constants.unidata
                    )
                )
                > 1
                and tree.findall(".//{%s}catalogRef" % constants.unidata) != []
            ):
                if self.nested_check is not True:
                    self.status = "Ninth Scenario"
                    return self.status
                else:
                    self.nested_num = 0
                    self.nested_num_temp = 0
                    self.nested_checker(url)

                    for i in self.all_dirs:
                        if i.count("/") > self.nested_num:
                            self.nested_num = i.count("/")
                    self.nested_num = self.nested_num + 1
                    self.status = "Ninth Scenario"
                    return self.status, self.nested_num
            # Fourth case:
            if (
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
                == []
                and tree.findall(".//{%s}catalogRef" % constants.unidata) == []
            ):
                self.status = "Fourth Scenario"
                return self.status
            if (
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
                != []
                and tree.findall(".//{%s}catalogRef" % constants.unidata) == []
            ):
                # Fifth to Seventh cases are here
                # THIS CONDITION SHOULD BE REFACTORED. I THINK BY REMOVING [@urlPath] FROM THE CONDITION IT WILL WORK
                if len(tree.findall(".//{%s}dataset" % constants.unidata)) > 1:
                    self.status = "Fifth Scenario"
                    return self.status
                else:
                    # Sixth and Seventh cases are here
                    dataset = tree.find("{%s}dataset" % constants.unidata)
                    metadata = dataset.find("{%s}metadata" % constants.unidata)

                    # Serviceså
                    service_tag = dataset.find(
                        "{%s}serviceName" % constants.unidata
                    )

                    if service_tag is None:
                        if metadata is not None:
                            service_tag = metadata.find(
                                "{%s}serviceName" % constants.unidata
                            )
                        else:
                            return "The dataset is not even Single or Aggregated dataset".__str__()

                    if service_tag is None:
                        # Use services found in the file. FMRC aggs do this.
                        services = tree.findall(
                            ".//{%s}service[@serviceType='Compound']"
                            % constants.unidata
                        )
                    else:
                        # Use specific named services    THIS PART SHOULD BE REFACTORED
                        services = tree.findall(
                            ".//{%s}service[@name='%s']"
                            % (constants.unidata, service_tag.text)
                        )

                    for i, service in enumerate(services):
                        # In TDS version 4 and 5 'Compound' is different
                        if (
                            service.get("serviceType") == "Compound"
                            or service.get("serviceType") == "compound"
                        ):
                            for s in service.findall(
                                "{%s}service" % constants.unidata
                            ):
                                if dataset.get("urlPath") is not None:
                                    service_url = utils.references_urls(
                                        url, s.get("base")
                                    ) + dataset.get("urlPath")
                                else:
                                    service_url = utils.references_urls(
                                        url, s.get("base")
                                    )
                                if s.get("name") == "http":
                                    a = requests.head(service_url)
                                    if "Content-Length" not in a.headers:
                                        self.status = "Seventh Scenario"
                                        return self.status
                                    else:
                                        self.status = "Sixth Scenario"
                                        return self.status

        # Second case:
        elif "catalogRef" in str(all_tags_list) and "dataset" not in str(
            all_tags_list
        ):
            if self.nested_check is not True:
                self.status = "Second Scenario"
                return self.status
            else:
                self.nested_num = 0
                self.nested_num_temp = 0
                self.nested_checker_exceptions(url)
                for i in self.all_href:
                    for j in self.all_href:
                        if i[0] in j[1]:
                            if j[0] not in self.all_dirs_extensions:
                                self.all_dirs_extensions.append(j[0])
                self.nested_num = len(self.all_dirs_extensions) + 1
                self.status = "Second Scenario"
                return self.status, self.nested_num
        # Eighth case:
        elif "catalogRef" in str(all_tags_list) and "dataset" in str(
            all_tags_list
        ):
            if self.nested_check is not True:
                self.status = "Eighth Scenario"
                return self.status
            else:
                self.nested_num = 0
                self.nested_num_temp = 0
                self.nested_checker_exceptions(url)
                for i in self.all_href:
                    for j in self.all_href:
                        if i[0] in j[1]:
                            if j[0] not in self.all_dirs_extensions:
                                self.all_dirs_extensions.append(j[0])

                self.nested_num = len(self.all_dirs_extensions) + 1
                self.status = "Eighth Scenario"
                return self.status, self.nested_num
        # Fourth case:
        elif "catalogRef" not in str(all_tags_list) and "dataset" not in str(
            all_tags_list
        ):
            if (
                tree.findall(".//{%s}dataset[@urlPath]" % constants.unidata)
                == []
                and tree.findall(".//{%s}catalogRef" % constants.unidata) == []
            ):
                self.status = "Fourth Scenario"
                return self.status

    def nested_checker(self, url: str):
        """
        A function for returning the depth of
        nested datasets in TDS for scenarios 1, 3,
        ,and 9
        """
        xml_url_catalog, id_catalog, xml = utils.xml_processing(
            url, self.requests_properties
        )
        try:
            tree = etree.XML(xml)
        except BaseException:
            return (
                "The Catalog is not reachable. Check the Catalg URL in the TDS"
            )

        for child in tree.findall(".//{%s}catalogRef" % constants.unidata):
            if "catalogRef" in str(child):
                self.nested_checker(
                    utils.references_urls(
                        url, child.get("{%s}href" % constants.w3)
                    )
                )
                url_modified = url.replace("catalog.xml", "").replace(
                    self.xml_url_catalog.replace("catalog.xml", ""), ""
                )
                if url_modified not in self.all_dirs:
                    self.all_dirs.append(
                        url.replace("catalog.xml", "").replace(
                            self.xml_url_catalog.replace("catalog.xml", ""), ""
                        )
                    )

    def nested_checker_exceptions(self, url: str):
        """
        A function for returning the depth of
        nested datasets in TDS for scenarios 2 and 8
        """
        xml_url_catalog, id_catalog, xml = utils.xml_processing(
            url, self.requests_properties
        )

        try:
            tree = etree.XML(xml)
        except BaseException:
            return (
                "The Catalog is not reachable. Check the Catalg URL in the TDS"
            )

        for child in tree.findall(".//{%s}catalogRef" % constants.unidata):
            if "catalogRef" in str(child):
                self.nested_checker_exceptions(
                    utils.references_urls(
                        url, child.get("{%s}href" % constants.w3)
                    )
                )

                if (
                    url,
                    [
                        utils.references_urls(
                            url, c.get("{%s}href" % constants.w3)
                        )
                        for c in tree.findall(
                            ".//{%s}catalogRef" % constants.unidata
                        )
                    ],
                ) not in self.all_href:
                    self.all_href.append(
                        (
                            url,
                            [
                                utils.references_urls(
                                    url, c.get("{%s}href" % constants.w3)
                                )
                                for c in tree.findall(
                                    ".//{%s}catalogRef" % constants.unidata
                                )
                            ],
                        )
                    )

    def __str__(self):
        return f"{self.status, self.nested_num}"
