# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

import json
import random

import pystac
import requests
from lxml import etree

from . import logger, utils
from .statics import constants


class Thumbnails(object):
    """
    This class is used to create thumbnail images for STAC-Collections and STAC-Items.
    """

    def collection(
        self,
        collection_thumbnail: str,
        collection_overview: str,
        services: etree.Element,
        dataset: dict,
        harvesting_vars: dict,
        collection_id: str,
        url: str,
        catalog: pystac.Catalog,
        collection_thumbnail_link: str,
        collection_overview_link: str,
        logger_properties: dict = dict(),
    ):
        """
        A function to create thumbnail images for STAC-Collections.

        Args:
            collection_thumbnail (str): The type of thumbnail image for STAC-Collections. It can be `wms` or `link`.
            collection_overview (str): The type of overview image for STAC-Collections. It can be `wms` or `link`.
            services (list): A list of services for STAC-Collections.
            dataset (dict): A dictionary of dataset information.
            harvesting_vars (dict): A dictionary of harvesting variables.
            collection_id (str): The ID of STAC-Collections.
            url (str): The URL of STAC-Catalog.
            catalog (pystac.Catalog): A STAC-Catalog.
            collection_thumbnail_link (str): The link of thumbnail image for STAC-Collections when `collection_thumbnail` or `collection_overview` set as `link`.
            collection_overview_link (str): The link of overview image for STAC-Collections when `collection_thumbnail` or `collection_overview` set as `link`.
            logger_properties (dict): A dictionary of logger properties. For more information, please see :class:`~tds2stac.logger.Logger` class.

        """
        collection: pystac.Collection = constants.empty_collection
        if logger_properties is not None:
            self.logger_properties = logger_properties

        if collection_thumbnail == "wms" or collection_overview == "wms":
            rand_idx = random.randrange(len(constants.colorbars))
            random_num = constants.colorbars[rand_idx]
            for service in services:
                if (
                    service.get("serviceType") == "Compound"
                    or service.get("serviceType") == "compound"
                ):
                    for s in service.findall(
                        "{%s}service" % constants.unidata
                    ):
                        if s.get("name") == "wms":
                            service_url = utils.references_urls(
                                url, s.get("base")
                            ) + dataset.get("urlPath")
                            minmax_url = (
                                service_url
                                + "?VERSION=1.1.1&REQUEST=GetMetadata&item=minmax&SRS=EPSG%3A4326&LAYERS="
                                + harvesting_vars["variable_ids"][0]
                                + "&BBOX="
                                + harvesting_vars["horizontal_extent_lon_min"]
                                + ","
                                + str(
                                    float(
                                        harvesting_vars[
                                            "horizontal_extent_lat_min"
                                        ]
                                    )
                                )
                                + ","
                                + harvesting_vars["horizontal_extent_lon_max"]
                                + ","
                                + str(
                                    float(
                                        harvesting_vars[
                                            "horizontal_extent_lat_max"
                                        ]
                                    )
                                )
                                + "&WIDTH=1000&HEIGHT=1000&FORMAT=image/png"
                                + "&TIME="
                                + harvesting_vars[
                                    "temporal_extent_start_datetime"
                                ]
                            )
                            get_minmax_head = requests.head(
                                minmax_url, timeout=10
                            )
                            if get_minmax_head.status_code == 200:
                                get_minmax = requests.get(
                                    minmax_url,
                                    None,
                                    verify=False,
                                    timeout=10,
                                )
                                minmax = json.loads(get_minmax.text)

                                min_color = minmax["min"]
                                max_color = minmax["max"]

                                thumbnail_url = (
                                    service_url
                                    + "?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG%3A4326&TRANSPARENT=TRUE&ABOVEMAXCOLOR=extend&BELOWMINCOLOR=extend&BGCOLOR=extend&LOGSCALE=false&&COLORSCALERANGE="
                                    + str(min_color)
                                    + ","
                                    + str(max_color)
                                    + "&STYLES=default-scalar/"
                                    + random_num
                                    + "&LAYERS="
                                    + harvesting_vars["variable_ids"][0]
                                    + "&BBOX="
                                    + harvesting_vars[
                                        "horizontal_extent_lon_min"
                                    ]
                                    + ","
                                    + str(
                                        float(
                                            harvesting_vars[
                                                "horizontal_extent_lat_min"
                                            ]
                                        )
                                    )
                                    + ","
                                    + harvesting_vars[
                                        "horizontal_extent_lon_max"
                                    ]
                                    + ","
                                    + str(
                                        float(
                                            harvesting_vars[
                                                "horizontal_extent_lat_max"
                                            ]
                                        )
                                    )
                                    + "&WIDTH=1000&HEIGHT=1000&FORMAT=image/png"
                                    + "&TIME="
                                    + harvesting_vars[
                                        "temporal_extent_start_datetime"
                                    ]
                                )
                            else:
                                self.logger_properties[
                                    "logger_level"
                                ] = "WARNING"
                                self.logger_properties["logger_msg"] = (
                                    "The getminmax thumbnail argument for "
                                    + collection_id
                                    + " is not available. It will be replaced by the default thumbnail."
                                )
                                logger.Logger(self.logger_properties)
                                thumbnail_url = (
                                    service_url
                                    + "?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG%3A4326&TRANSPARENT=TRUE&ABOVEMAXCOLOR=extend&BELOWMINCOLOR=extend&BGCOLOR=extend&LOGSCALE=false&STYLES=default-scalar/"
                                    + random_num
                                    + "&LAYERS="
                                    + harvesting_vars["variable_ids"][0]
                                    + "&BBOX="
                                    + harvesting_vars[
                                        "horizontal_extent_lon_min"
                                    ]
                                    + ","
                                    + str(
                                        float(
                                            harvesting_vars[
                                                "horizontal_extent_lat_min"
                                            ]
                                        )
                                    )
                                    + ","
                                    + harvesting_vars[
                                        "horizontal_extent_lon_max"
                                    ]
                                    + ","
                                    + str(
                                        float(
                                            harvesting_vars[
                                                "horizontal_extent_lat_max"
                                            ]
                                        )
                                    )
                                    + "&WIDTH=1000&HEIGHT=1000&FORMAT=image/png"
                                    + "&TIME="
                                    + harvesting_vars[
                                        "temporal_extent_start_datetime"
                                    ]
                                )
                            head_of_thumbnail = requests.head(
                                thumbnail_url, timeout=10
                            )
                            if head_of_thumbnail.status_code == 200:
                                if collection_thumbnail in ["wms"]:
                                    collection = catalog.get_child(collection_id)  # type: ignore
                                    collection.add_asset(
                                        key="thumbnail",
                                        asset=pystac.Asset(
                                            href=thumbnail_url,
                                            roles=["thumbnail"],
                                            # title=without_slash,
                                            media_type=pystac.MediaType.PNG,
                                        ),
                                    )
                                if collection_overview in ["wms"]:
                                    collection = catalog.get_child(collection_id)  # type: ignore
                                    collection.add_asset(
                                        key="rendered_preview",
                                        asset=pystac.Asset(
                                            href=thumbnail_url,
                                            roles=["visual"],
                                            # title=collection_id,
                                            media_type=pystac.MediaType.PNG,
                                        ),
                                    )
                            else:
                                self.logger_properties[
                                    "logger_level"
                                ] = "ERROR"
                                self.logger_properties["logger_msg"] = (
                                    "The thumbnail image for "
                                    + collection_id
                                    + " is not available."
                                )
                                logger.Logger(self.logger_properties)

        if (
            collection_thumbnail == "link"
            and collection_thumbnail_link is not None
        ):
            collection = catalog.get_child(collection_id)  # type: ignore
            collection.add_asset(
                key="thumbnail",
                asset=pystac.Asset(
                    href=collection_thumbnail_link,
                    roles=["thumbnail"],
                    title=collection_id,
                    media_type=pystac.MediaType.PNG,
                ),
            )
        if (
            collection_overview == "link"
            and collection_overview_link is not None
        ):
            collection = catalog.get_child(collection_id)  # type: ignore
            collection.add_asset(
                key="rendered_preview",
                asset=pystac.Asset(
                    href=collection_overview_link,
                    roles=["visual"],
                    # title=collection_id,
                    media_type=pystac.MediaType.PNG,
                ),
            )

    def item(
        self,
        service: etree.Element,
        dataset: dict,
        harvesting_vars: dict,
        url: str,
        item: pystac.Item,
        item_thumbnail: bool,
        item_overview: bool,
        item_getminmax_thumbnail: bool,
        logger_properties: dict = dict(),
    ):
        """
        A function to create thumbnail images for STAC-Items.

        Args:
            service (list): A list of services for STAC-Items.
            dataset (dict): A dictionary of dataset information.
            harvesting_vars (dict): A dictionary of harvesting variables.
            url (str): The URL of STAC-Catalog.
            item (pystac.Item): A STAC-Item.
            item_thumbnail (bool): A boolean to create thumbnail image for STAC-Items.
            item_overview (bool): A boolean to create overview image for STAC-Items.
            item_getminmax_thumbnail (bool): A boolean to create thumbnail image for STAC-Items based on minmax.
            logger_properties (dict): A dictionary of logger properties. For more information, please see :class:`~tds2stac.logger.Logger` class.
        """
        rand_idx = random.randrange(len(constants.colorbars))
        random_num = constants.colorbars[rand_idx]
        if logger_properties is not None:
            self.logger_properties = logger_properties
        for s in service.findall("{%s}service" % constants.unidata):
            if (
                s.get("name") == "wms"
                and (item_thumbnail is True or item_overview is True)
                and item_getminmax_thumbnail is not True
            ):
                service_url = utils.references_urls(
                    url, s.get("base")
                ) + dataset.get("urlPath")
                thumbnail_url = (
                    service_url
                    + "?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG%3A4326&TRANSPARENT=TRUE&ABOVEMAXCOLOR=extend&BELOWMINCOLOR=extend&BGCOLOR=extend&LOGSCALE=false&STYLES=default-scalar/"
                    + random_num
                    + "&LAYERS="
                    + harvesting_vars["variable_ids"][0]
                    + "&BBOX="
                    + harvesting_vars["horizontal_extent_lon_min"]
                    + ","
                    + str(float(harvesting_vars["horizontal_extent_lat_min"]))
                    + ","
                    + harvesting_vars["horizontal_extent_lon_max"]
                    + ","
                    + str(float(harvesting_vars["horizontal_extent_lat_max"]))
                    + "&WIDTH=1000&HEIGHT=1000&FORMAT=image/png"
                    + "&TIME="
                    + harvesting_vars["temporal_extent_start_datetime"]
                )
                item_request = requests.head(thumbnail_url, timeout=10)
                if item_request.status_code == 200:
                    if item_thumbnail is True:
                        item.add_asset(
                            key="thumbnail",
                            asset=pystac.Asset(
                                href=thumbnail_url,
                                roles=["thumbnail"],
                                # title=without_slash,
                                media_type=pystac.MediaType.PNG,
                            ),
                        )
                    if item_overview is True:
                        item.add_asset(
                            key="rendered_preview",
                            asset=pystac.Asset(
                                href=thumbnail_url,
                                roles=["overview"],
                                # title=without_slash,
                                media_type=pystac.MediaType.PNG,
                            ),
                        )

                else:
                    self.logger_properties["logger_level"] = "ERROR"
                    self.logger_properties["logger_msg"] = (
                        "The thumbnail image for "
                        + item.id
                        + " is not available."
                    )
                    logger.Logger(self.logger_properties)

            if (
                s.get("name") == "wms"
                and (item_thumbnail is True or item_overview is True)
                and item_getminmax_thumbnail is True
            ):
                service_url = utils.references_urls(
                    url, s.get("base")
                ) + dataset.get("urlPath")
                minmax_url = (
                    service_url
                    + "?VERSION=1.1.1&REQUEST=GetMetadata&item=minmax&SRS=EPSG%3A4326&LAYERS="
                    + harvesting_vars["variable_ids"][0]
                    + "&BBOX="
                    + harvesting_vars["horizontal_extent_lon_min"]
                    + ","
                    + str(float(harvesting_vars["horizontal_extent_lat_min"]))
                    + ","
                    + harvesting_vars["horizontal_extent_lon_max"]
                    + ","
                    + str(float(harvesting_vars["horizontal_extent_lat_max"]))
                    + "&WIDTH=1000&HEIGHT=1000&FORMAT=image/png"
                    + "&TIME="
                    + harvesting_vars["temporal_extent_start_datetime"]
                )

                get_minmax_head = requests.head(minmax_url, timeout=10)
                if get_minmax_head.status_code == 200:
                    get_minmax = requests.get(minmax_url, None, verify=False)

                    minmax = json.loads(get_minmax.text)

                    min_color = minmax["min"]
                    max_color = minmax["max"]

                    thumbnail_url = (
                        service_url
                        + "?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG%3A4326&TRANSPARENT=TRUE&ABOVEMAXCOLOR=extend&BELOWMINCOLOR=extend&BGCOLOR=extend&LOGSCALE=false&&COLORSCALERANGE="
                        + str(min_color)
                        + ","
                        + str(max_color)
                        + "&STYLES=default-scalar/"
                        + random_num
                        + "&LAYERS="
                        + harvesting_vars["variable_ids"][0]
                        + "&BBOX="
                        + harvesting_vars["horizontal_extent_lon_min"]
                        + ","
                        + str(
                            float(harvesting_vars["horizontal_extent_lat_min"])
                        )
                        + ","
                        + harvesting_vars["horizontal_extent_lon_max"]
                        + ","
                        + str(
                            float(harvesting_vars["horizontal_extent_lat_max"])
                        )
                        + "&WIDTH=1000&HEIGHT=1000&FORMAT=image/png"
                        + "&TIME="
                        + harvesting_vars["temporal_extent_start_datetime"]
                    )
                else:
                    self.logger_properties["logger_level"] = "WARNING"
                    self.logger_properties["logger_msg"] = (
                        "The getminmax thumbnail argument for "
                        + item.id
                        + " is not available. It will be replaced by the default thumbnail."
                    )
                    logger.Logger(self.logger_properties)

                    thumbnail_url = (
                        service_url
                        + "?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG%3A4326&TRANSPARENT=TRUE&ABOVEMAXCOLOR=extend&BELOWMINCOLOR=extend&BGCOLOR=extend&LOGSCALE=false&STYLES=default-scalar/"
                        + random_num
                        + "&LAYERS="
                        + harvesting_vars["variable_ids"][0]
                        + "&BBOX="
                        + harvesting_vars["horizontal_extent_lon_min"]
                        + ","
                        + str(
                            float(harvesting_vars["horizontal_extent_lat_min"])
                        )
                        + ","
                        + harvesting_vars["horizontal_extent_lon_max"]
                        + ","
                        + str(
                            float(harvesting_vars["horizontal_extent_lat_max"])
                        )
                        + "&WIDTH=1000&HEIGHT=1000&FORMAT=image/png"
                        + "&TIME="
                        + harvesting_vars["temporal_extent_start_datetime"]
                    )
                item_request = requests.head(thumbnail_url, timeout=10)
                if item_request.status_code == 200:
                    if item_thumbnail is True:
                        item.add_asset(
                            key="thumbnail",
                            asset=pystac.Asset(
                                href=thumbnail_url,
                                roles=["thumbnail"],
                                # title=without_slash,
                                media_type=pystac.MediaType.PNG,
                            ),
                        )
                    if item_overview is True:
                        item.add_asset(
                            key="rendered_preview",
                            asset=pystac.Asset(
                                href=thumbnail_url,
                                roles=["overview"],
                                # title=without_slash,
                                media_type=pystac.MediaType.PNG,
                            ),
                        )
                else:
                    self.logger_properties["logger_level"] = "ERROR"
                    self.logger_properties["logger_msg"] = (
                        "The thumbnail image for "
                        + item.id
                        + " is not available."
                    )
                    logger.Logger(self.logger_properties)
