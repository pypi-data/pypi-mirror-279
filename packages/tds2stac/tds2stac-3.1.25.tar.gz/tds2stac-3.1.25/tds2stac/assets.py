# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0


from typing import Union
from urllib import parse as urlparse
from urllib.parse import quote_plus

import pystac
import requests

from . import utils
from .statics import constants
from .thumbnails import Thumbnails


class Assets:
    """
    This class is tasked with the responsibility of incorporating
    assets into STAC-Collections and STAC-Items.
    """

    def item(
        self,
        harvesting_vars: dict,
        item: pystac.Item,
        url: str,
        Recognizer_output: Union[str, None] = None,
        aggregated_dataset_url: Union[str, None] = None,
        asset_properties: Union[dict, None] = dict(),
        logger_properties: dict = dict(),
    ):
        """
        This is a function for adding assets to STAC-Items.

        Args:
            harvesting_vars (dict): A dictionary containing the variables required for harvesting.
            item (pystac.Item): A STAC-Item.
            Recognizer_output (dict): A dictionary containing the scenario output of the :class:`~tds2stac.Recognizer`.
            aggregated_dataset_url (str): The URL of the aggregated dataset.
            url (str): The URL of the catalog. It will be used for thumbnails
            asset_properties (dict): A dictionary containing the properties of the assets for more information refer to :class:`~tds2stac.TDS2STACIntegrator.asset_properties`.
            logger_properties (dict): A dictionary containing the properties of the logger for more information refer to :class:`~tds2stac.TDS2STACIntegrator.logger_properties`.
        """
        # Adding web services as assets into items
        if logger_properties is not None:
            self.logger_properties = logger_properties
        media_type_: Union[str, pystac.MediaType] = ""
        # for service in harvesting_vars["services"]:
        #     print(harvesting_vars["services_tuples"])

        #     if (
        #         service.get("serviceType") == "Compound"
        #         or service.get("serviceType") == "compound"
        #     ):
        if (
            asset_properties is not None
            and asset_properties.get("jupyter_notebook") is True
        ):
            catalog_path = urlparse.urlsplit(url).path.replace(
                "/thredds/catalog/", ""
            )
            additional = "/thredds/notebook/"
            service_url_notebook = utils.references_urls(
                url, additional
            ) + harvesting_vars["dataset"].get("ID")
            item.add_asset(
                key="jupyter_notebook",
                asset=pystac.Asset(
                    href=service_url_notebook
                    + "?catalog=%s&filename=%s"
                    % (catalog_path, "default_viewer.ipynb"),
                    title="Jupyter Notebook",
                    media_type=pystac.MediaType.HTML,
                ),
            )
        for s in harvesting_vars["services_tuples"]:
            service_url = utils.references_urls(url, s[0]) + harvesting_vars[
                "dataset"
            ].get("urlPath")

            if s[1] is not None:
                service_url += s[1]
            name_str: str = str(s[2])
            if s[2] in [
                "iso",
                "ncml",
                "uddc",
            ]:
                service_url += "?dataset=%s&&catalog=%s" % (
                    harvesting_vars["catalog_id"],
                    quote_plus(harvesting_vars["catalog_url"]),
                )
            elif s[2] in [
                "wms",
            ]:
                if (
                    asset_properties is not None
                    and asset_properties.get("explore_data") is True
                    and asset_properties.get("verify_explore_data") is not True
                ):
                    item.add_asset(
                        key="explore_data",
                        asset=pystac.Asset(
                            href=utils.references_urls(
                                url, "/thredds/Godiva.html"
                            )
                            + "?server="
                            + service_url,
                            title="Explore Data",
                            media_type=pystac.MediaType.HTML,
                        ),
                    )
                elif (
                    asset_properties is not None
                    and asset_properties.get("explore_data") is True
                    and asset_properties.get("verify_explore_data") is True
                ):
                    head = requests.head(
                        service_url + "?request=GetMetadata&item=menu"
                    )
                    if head.status_code == 200:
                        item.add_asset(
                            key="explore_data",
                            asset=pystac.Asset(
                                href=utils.references_urls(
                                    url, "/thredds/Godiva.html"
                                )
                                + "?server="
                                + service_url,
                                title="Explore Data",
                                media_type=pystac.MediaType.HTML,
                            ),
                        )
                service_url += (
                    "?service=WMS&version=1.3.0&request=GetCapabilities"
                )
            elif (
                s[2]
                in [
                    "http",
                ]
                and "Seventh Scenario" in str(Recognizer_output)
                and aggregated_dataset_url is not None
            ):
                service_url = aggregated_dataset_url
                media_type_ = pystac.MediaType.HTML
            elif (
                s[2]
                in [
                    "http",
                ]
                and "Seventh Scenario" in str(Recognizer_output)
                and aggregated_dataset_url is None
            ):
                # service_url += "?service=WMS&version=1.3.0&request=GetCapabilities"
                media_type_ = pystac.MediaType.HTML

            if s[2] in ["odap"]:
                service_url += ".html"
            # Determinatio of Media Type
            if s[2] in [
                "iso",
                "ncml",
                "wms",
                "wcs",
                "wfs",
                "sos",
            ]:
                media_type_ = pystac.MediaType.XML
            elif s[2] in ["http"] and "Seventh Scenario" not in str(
                Recognizer_output
            ):
                media_type_ = "application/netcdf"
            elif s[2] in [
                "dap4",
                "odap",
                "uddc",
            ]:
                media_type_ = pystac.MediaType.HTML
            else:
                media_type_ = pystac.MediaType.TEXT

            if asset_properties is None or (
                (
                    asset_properties.get("assets_list_allowed") is None
                    or asset_properties.get("assets_list_allowed") == []
                    or isinstance(
                        asset_properties.get("assets_list_allowed"),
                        str,
                    )
                )
                and (
                    asset_properties.get("assets_list_avoided") is None
                    or asset_properties.get("assets_list_avoided") == []
                    or isinstance(
                        asset_properties.get("assets_list_avoided"),
                        str,
                    )
                )
            ):
                item.add_asset(
                    key=s[2],
                    asset=pystac.Asset(
                        href=service_url,
                        # title=without_slash,
                        media_type=media_type_,
                    ),
                )

            elif (
                asset_properties is not None
                and (
                    asset_properties.get("assets_list_allowed") is not None
                    and isinstance(
                        asset_properties.get("assets_list_allowed"),
                        list,
                    )
                )
                and (
                    asset_properties.get("assets_list_avoided") is not None
                    and isinstance(
                        asset_properties.get("assets_list_avoided"),
                        list,
                    )
                )
            ):
                if name_str in (  # type: ignore
                    asset_properties.get("assets_list_allowed")
                ) and name_str not in (  # type: ignore
                    asset_properties.get("assets_list_avoided")
                ):
                    item.add_asset(
                        key=s[2],
                        asset=pystac.Asset(
                            href=service_url,
                            # title=without_slash,
                            media_type=media_type_,
                        ),
                    )
            elif (
                asset_properties is not None
                and (
                    asset_properties.get("assets_list_allowed") is None
                    or asset_properties.get("assets_list_allowed") == []
                    or isinstance(
                        asset_properties.get("assets_list_allowed"),
                        str,
                    )
                )
                and (
                    asset_properties.get("assets_list_avoided") is not None
                    and isinstance(
                        asset_properties.get("assets_list_avoided"),
                        list,
                    )
                )
            ):
                if name_str not in (asset_properties.get("assets_list_avoided")):  # type: ignore
                    item.add_asset(
                        key=s[2],
                        asset=pystac.Asset(
                            href=service_url,
                            # title=without_slash,
                            media_type=media_type_,
                        ),
                    )
            elif (
                asset_properties is not None
                and (
                    asset_properties.get("assets_list_allowed") is not None
                    and isinstance(
                        asset_properties.get("assets_list_allowed"),
                        list,
                    )
                )
                and (
                    asset_properties.get("assets_list_avoided") is None
                    or asset_properties.get("assets_list_avoided") == []
                    or isinstance(
                        asset_properties.get("assets_list_avoided"),
                        str,
                    )
                )
            ):
                if name_str in (asset_properties.get("assets_list_allowed")):  # type: ignore
                    item.add_asset(
                        key=s[2],
                        asset=pystac.Asset(
                            href=service_url,
                            # title=without_slash,
                            media_type=media_type_,
                        ),
                    )
            if asset_properties is not None:
                if asset_properties.get("item_thumbnail") is not None:
                    thumbnail = Thumbnails()
                    thumbnail.item(
                        harvesting_vars["services"][0],
                        harvesting_vars["dataset"],
                        harvesting_vars,
                        url,
                        item,
                        asset_properties["item_thumbnail"],
                        asset_properties["item_overview"],
                        asset_properties["item_getminmax_thumbnail"],
                        logger_properties=self.logger_properties,
                    )
                if asset_properties.get("item_custom_asset") is not None:
                    for asset in asset_properties["item_custom_asset"]:
                        item.add_asset(
                            key=asset.get("key"),
                            asset=pystac.Asset(
                                href=asset.get("href"),
                                title=asset.get("title")
                                if asset.get("title") is not None
                                else asset.get("key"),
                                roles=asset["roles"]
                                if asset.get("roles") is not None
                                else ["data"],
                                media_type=asset["media_type"]
                                if asset.get("media_type") is not None
                                else pystac.MediaType.TEXT,
                            ),
                        )
            # print(s.get("base"), s.get("suffix"), s.get("name"),service_url)
            # s.clear()
            # service.clear()

    def collection(
        self,
        harvesting_vars: dict,
        collection_dict: dict,
        stac_catalog: pystac.Catalog,
        asset_properties: dict = dict(),
        logger_properties: dict = dict(),
    ):
        """
        This is a function for adding assets to STAC-Collections.

        Args:
            asset_properties (dict): A dictionary containing the properties of the assets for more information refer to :class:`~tds2stac.TDS2STACIntegrator.asset_properties`.
            harvesting_vars (dict): A dictionary containing the variables required for harvesting.
            collection_dict (dict): A dictionary containing the properties of the collection.
            stac_catalog (pystac.Catalog): A STAC-Catalog.
            logger_properties (dict): A dictionary containing the properties of the logger for more information refer to :class:`~tds2stac.TDS2STACIntegrator.logger_properties`.


        """
        if logger_properties is not None:
            self.logger_properties = logger_properties

        if asset_properties is not None:
            if (
                asset_properties.get("collection_thumbnail") is not None
                or asset_properties.get("collection_overview") is not None
            ):
                thumbnail = Thumbnails()
                thumbnail.collection(
                    asset_properties["collection_thumbnail"],
                    asset_properties["collection_overview"],
                    dict(harvesting_vars)["services"],
                    dict(harvesting_vars)["dataset"],
                    dict(harvesting_vars),
                    dict(collection_dict)["collection_id"],
                    dict(harvesting_vars)["main_dataset_url"],
                    stac_catalog,
                    str(asset_properties.get("collection_thumbnail_link")),
                    str(asset_properties.get("collection_overview_link")),
                    logger_properties=self.logger_properties,
                )
            if asset_properties.get("collection_custom_asset") is not None:
                collection: pystac.Collection = constants.empty_collection
                collection = stac_catalog.get_child(dict(collection_dict)["collection_id"])  # type: ignore
                for asset in asset_properties["collection_custom_asset"]:
                    collection.add_asset(
                        key=asset.get("key"),
                        asset=pystac.Asset(
                            href=asset.get("href"),
                            title=asset.get("title")
                            if asset.get("title") is not None
                            else asset.get("key"),
                            roles=asset.get("roles")
                            if asset.get("roles") is not None
                            else ["data"],
                            media_type=asset.get("media_type")
                            if asset.get("media_type") is not None
                            else pystac.MediaType.TEXT,
                        ),
                    )
