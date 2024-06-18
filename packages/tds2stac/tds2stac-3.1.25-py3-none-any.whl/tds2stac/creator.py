import importlib
import inspect

# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
import os
import sys

# import traceback
from datetime import datetime
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from typing import Union

import pystac
from shapely import geometry

from . import assets, logger, utils
from .analysers.existence_validator import ExistenceValidator
from .extensions import common_metadata, datacube
from .extensions.extra_metadata import ExtraMetadata
from .statics import constants


class STACCreator(object):
    """
    A class for creating STAC catalog, -Collections
    and its -Items from TDS datasets catalogs.
    """

    def STACCatalog(
        self,
        url: str,
        stac_id: str,
        stac_title: Union[str, None],
        stac_desc: Union[str, None],
        stac_dir: str,
        stac_existence: bool = False,
        logger_properties: dict = dict(),
        requests_properties: dict = dict(),
    ):
        """
        A function for creating STAC catalog from TDS dataset catalog.

        Args:
            url: The URL of the TDS catalog.
            stac_id: The ID of the STAC catalog.
            stac_title: The title of the STAC catalog.
            stac_desc: The description of the STAC catalog.
            stac_dir: The directory of saving the STAC catalog.
            stac_existence: If it is True, it means that the STAC catalog
                already exists in the directory and for the harvesting, there
                is no need to create a new STAC-Catalog and import new collections
                In the existed STAC-Catalog. False by default.
            logger_properties: The properties of the logger. For more information please check the :class:`~tds2stac.logger.Logger` class.
            requests_properties: The properties of the requests. For more information please check the :class:`~tds2stac.TDS2STAC.requests_properties` class.
        """
        # using 'xml_processing' we get the catalog URL with
        # XML extension and catalog id and XML content of TDS catalog.
        catalog: dict = dict()

        if logger_properties is not None:
            self.logger_properties = logger_properties
        xml_url_catalog, id_catalog, xml = utils.xml_processing(
            url, requests_properties
        )
        if stac_desc is None:
            stac_desc = "This is a STAC catalog created by tds2stac"

        # In the following if condition we are going to create a new STAC catalog or use the existed one.
        if stac_existence is True:
            if stac_dir is None:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "You have turned on the `stac_existence`, so please provide the directory of the existed STAC catalog"
                logger.Logger(self.logger_properties)
                return
            else:
                if ExistenceValidator(stac_dir).existence is True:
                    self.logger_properties["logger_level"] = "INFO"
                    self.logger_properties[
                        "logger_msg"
                    ] = "The STAC catalog already exists in the directory"
                    logger.Logger(self.logger_properties)
                    id_catalog = pystac.Catalog.from_file(
                        stac_dir + "/catalog.json"
                    ).id
                    catalog[id_catalog] = pystac.Catalog.from_file(
                        stac_dir + "/catalog.json"
                    )
                else:
                    self.logger_properties["logger_level"] = "INFO"
                    self.logger_properties[
                        "logger_msg"
                    ] = "The STAC catalog does not exist in the directory"
                    logger.Logger(self.logger_properties)
                    id_catalog = id_catalog + " Catalog"
                    catalog[id_catalog] = pystac.Catalog(
                        id=stac_id,
                        title=stac_title,
                        description="["
                        + stac_desc
                        + "]("
                        + utils.xml2html(xml_url_catalog)
                        + ")",
                    )
        else:
            self.logger_properties["logger_level"] = "INFO"
            self.logger_properties[
                "logger_msg"
            ] = "It creates a new catalog in the directory"
            logger.Logger(self.logger_properties)
            id_catalog = id_catalog + " Catalog"
            catalog[id_catalog] = pystac.Catalog(
                id=stac_id,
                title=stac_title,
                description="["
                + stac_desc
                + "]("
                + utils.xml2html(xml_url_catalog)
                + ")",
            )
        return catalog[id_catalog]

    def STACCollection(
        self,
        catalog: pystac.Catalog,
        collection_id: str,
        collection_title: str,
        collection_description: str,
        # collection_scientific: bool = False,
        stac_existence_collection: bool = False,
        logger_properties: dict = dict(),
        extra_metadata: dict = dict(),
    ):
        """
        This is a function for creating STAC collection
        from harvested information from TDS dataset catalog.
        This function returns a dictionary with two keys:
            1. collection: The STAC collection

            2. existed_items_id_list: The list of the items that already
            exist in the STAC collection and it is going to be used for
            the harvesting process.

        Args:
            catalog: The STAC catalog.
            collection_id: The ID of the STAC collection.
            collection_title: The title of the STAC collection.
            collection_description: The description of the STAC collection.
            collection_scientific: The scientific extension of the STAC collection.
            stac_existence_collection: If it is True, it means that the STAC collection
                already exists in the catalog and for the harvesting, there
                is no need to create a new STAC-Collection and import new items
                In the existed STAC-Collection. False by default.
            logger_properties: The properties of the logger. For more information please check the :class:`~tds2stac.logger.Logger` class.
        """
        collection: dict = dict()
        collection["collection_bbox_existed"] = None
        collection["collection_interval_time_final_existed"] = None
        existed_items_id_list = []
        if logger_properties is not None:
            self.logger_properties = logger_properties
        if stac_existence_collection is True:
            existed_collections_id_list = []
            existed_collections_id_list = [
                existence_collection.id
                for existence_collection in list(catalog.get_collections())
            ]
            if (
                collection is not None
                and collection_id in existed_collections_id_list
            ):
                collection[collection_id] = catalog.get_child(collection_id)
                collection["collection_bbox_existed"] = collection[
                    collection_id
                ].extent.spatial.bboxes[0]
                collection[
                    "collection_interval_time_final_existed"
                ] = collection[collection_id].extent.temporal.intervals[0]
                existed_items_id_list = [
                    existed_item.id
                    for existed_item in list(
                        collection[collection_id].get_items()
                    )
                ]
            else:
                # Defining a None Spatial and Temporal extent for the collection
                collection[collection_id] = pystac.Collection(
                    id=collection_id,
                    title=collection_title,
                    extent=pystac.Extent(
                        spatial=pystac.SpatialExtent(bboxes=[0.0, 0.0]),
                        temporal=pystac.TemporalExtent(
                            intervals=[[datetime.utcnow(), datetime.utcnow()]]
                        ),
                    ),
                    description=collection_description,
                )
                if extra_metadata is not None:
                    if extra_metadata.get("extra_metadata"):
                        ExtraMetadata(
                            logger_properties=self.logger_properties
                        ).collection(
                            collection=collection[collection_id],
                            extra_metadata=extra_metadata,
                        )
                    else:
                        self.logger_properties["logger_level"] = "INFO"
                        self.logger_properties[
                            "logger_msg"
                        ] = "The `extra_metadata` is not activated. So, it does not add any extra metadata to the STAC collection."
                        # logger.Logger(self.logger_properties)

                catalog.add_child(collection[collection_id])

        else:
            # When the STAC collection does not exist in the catalog
            # Instead of None value for Spatial and Temporal extent, we define a default value
            # as a list of [0.0, 0.0] for Spatial extent and [[datetime.utcnow(), datetime.utcnow()]] for Temporal extent
            collection[collection_id] = pystac.Collection(
                id=collection_id,
                title=collection_title,
                extent=pystac.Extent(
                    spatial=pystac.SpatialExtent(bboxes=[0.0, 0.0]),
                    temporal=pystac.TemporalExtent(
                        intervals=[[datetime.utcnow(), datetime.utcnow()]]
                    ),
                ),
                description=collection_description,
            )

            if extra_metadata is not None:
                if extra_metadata.get("extra_metadata"):
                    ExtraMetadata(
                        logger_properties=self.logger_properties
                    ).collection(
                        collection=collection[collection_id],
                        extra_metadata=extra_metadata,
                    )
                else:
                    self.logger_properties["logger_level"] = "INFO"
                    self.logger_properties[
                        "logger_msg"
                    ] = "The `extra_metadata` is not activated. So, it does not add any extra metadata to the STAC collection."
                    # logger.Logger(self.logger_properties)

            catalog.add_child(collection[collection_id])

        # if collection_scientific is True:
        #     scientific_class = scientific.Scientific()
        #     scientific_class.collection(
        #         catalog.get_child(collection_id),
        #         collection_scientific,
        #     )
        return {
            "existed_items_id_list": existed_items_id_list,
            "collection": collection[collection_id],
            "collection_bbox_existed": collection["collection_bbox_existed"],
            "collection_interval_time_final_existed": collection[
                "collection_interval_time_final_existed"
            ],
        }

    def STACItem(
        self,
        url: str,
        catalog: pystac.Catalog,
        harvesting_vars: dict,
        Recognizer_output: Union[str, None],
        collection_id: str,
        aggregated_dataset_url: Union[str, None] = None,
        extension_properties: Union[dict, None] = None,
        asset_properties: Union[dict, None] = dict(),
        logger_properties: dict = dict(),
        extra_metadata: dict = dict(),
        stac_existence_collection: bool = False,
        collection_bbox_existed: Union[list, None] = None,
        collection_interval_time_final_existed: Union[list, None] = None,
    ):
        """
        This is a function for creating STAC item
        from harvested data in TDS dataset catalog.

        Args:
            url: The URL of the TDS catalog.
            catalog: The STAC catalog.
            harvesting_vars: The harvested data from TDS catalog.
            Recognizer_output: The output of the Recognizer class.
            collection_id: The ID of the STAC collection.
            aggregated_dataset_url: The URL of the aggregated dataset that
                whole of data is located there.
            extension_properties: The properties of the extensions.
            asset_properties: The properties of the assets.
            logger_properties: The properties of the logger. For more information please check the :class:`~tds2stac.logger.Logger` class.
        """
        # if "Seventh Scenario" in str(Recognizer_output):
        #     service_url_html = utils.xml2html(url)
        # else:
        #     service_url_html = (
        #         utils.xml2html(url)
        #         + "?dataset="
        #         + harvesting_vars["dataset"].get("ID")
        #     )

        if logger_properties is not None:
            self.logger_properties = logger_properties
        if (
            utils.replacement_func_collection_item_id(
                harvesting_vars["item_id"]
            )
            is None
            or harvesting_vars["item_footprint"] is None
            or harvesting_vars["item_bbox"] is None
            or harvesting_vars["modified_date_time"] is None
        ):
            self.logger_properties["logger_level"] = "CRITICAL"
            self.logger_properties[
                "logger_msg"
            ] = "One of `item_id`, `item_footprint`, `item_bbox` or `modified_date_time` is None, so you need to double check your dataset."
            logger.Logger(self.logger_properties)
            return
        item = pystac.Item(
            id=utils.replacement_func_collection_item_id(
                harvesting_vars["item_id"]
            ),
            geometry=geometry.mapping(harvesting_vars["item_footprint"]),
            bbox=harvesting_vars["item_bbox"],
            datetime=harvesting_vars["modified_date_time"],
            properties={},
        )

        if (
            extension_properties is not None
            and extension_properties["item_common_metadata"] is True
        ):
            common_metadata_class = common_metadata.CommonMetadata()
            common_metadata_class.item(
                item, harvesting_vars, self.logger_properties
            )

        #########################################
        # Adding web services as assets into items
        #########################################
        # profiler = cProfile.Profile()
        # profiler.enable()

        asset = assets.Assets()
        asset.item(
            harvesting_vars=harvesting_vars,
            item=item,
            Recognizer_output=Recognizer_output,
            url=url,
            aggregated_dataset_url=aggregated_dataset_url,
            asset_properties=asset_properties,
            logger_properties=self.logger_properties,
        )
        # profiler.disable()
        # stats = pstats.Stats(profiler).sort_stats('cumtime')
        # stats.print_stats()

        if extension_properties is not None:
            if extension_properties.get("item_extensions") is not None:
                for extension_property in extension_properties[
                    "item_extensions"
                ]:
                    # if (
                    #     isinstance(extension_property, str)
                    #     and extension_property == "item_scientific"
                    # ):
                    #     scientific_class = scientific.Scientific()
                    #     scientific_class.item(
                    #         item, extension_properties["item_scientific"]
                    #     )
                    if (
                        isinstance(extension_property, str)
                        and extension_property == "item_datacube_extension"
                    ):
                        datacube_class = datacube.Datacube()
                        datacube_class.item_extension(
                            item, harvesting_vars, self.logger_properties
                        )
                    if (
                        isinstance(extension_property, str)
                        and extension_property == "common_metadata"
                    ):
                        common_metadata_class = (
                            common_metadata.CommonMetadata()
                        )
                        common_metadata_class.item(
                            item, harvesting_vars, self.logger_properties
                        )
                    if isinstance(extension_property, tuple):
                        if (
                            len(extension_property) < 2
                            or len(extension_property) > 3
                        ):
                            self.logger_properties["logger_level"] = "ERROR"
                            self.logger_properties[
                                "logger_msg"
                            ] = "The length of `extension_property` tuple is less than 2 or greater than 3, so you need to double check your input"
                            logger.Logger(self.logger_properties)
                            return
                        elif len(extension_property) == 2:
                            caller_filename = inspect.stack()
                            script_path = caller_filename[2][1]
                            sys.path.append(script_path)
                            custom_module = os.path.splitext(
                                os.path.basename(caller_filename[2][1])
                            )[0]
                            imported_module = importlib.import_module(
                                custom_module
                            )

                        elif len(extension_property) == 3:
                            script_path_dir = os.path.dirname(
                                extension_property[2]
                            )
                            sys.path.append(script_path_dir)
                            custom_module = os.path.splitext(
                                os.path.basename(extension_property[2])
                            )[0]
                            # imported_module = importlib.import_module(
                            #     custom_module
                            # )
                            try:
                                spec = spec_from_loader(
                                    custom_module,
                                    SourceFileLoader(
                                        custom_module, extension_property[2]
                                    ),
                                )
                                imported_module = module_from_spec(spec)  # type: ignore
                                spec.loader.exec_module(imported_module)  # type: ignore
                            except Exception:
                                self.logger_properties[
                                    "logger_level"
                                ] = "ERROR"
                                self.logger_properties[
                                    "logger_msg"
                                ] = "Check your extension script path, third element of the tuple"
                                logger.Logger(self.logger_properties)
                                return

                        if "." in extension_property[1]:
                            extension_property_class_str = extension_property[
                                1
                            ].split(".")[0]
                            extension_property_function_str = (
                                extension_property[1].split(".")[1]
                            )
                            if hasattr(
                                imported_module, extension_property_class_str
                            ):
                                extension_property_class = getattr(
                                    imported_module,
                                    extension_property_class_str,
                                )
                                instance = extension_property_class()
                                if hasattr(
                                    instance, extension_property_function_str
                                ):
                                    a = getattr(
                                        instance,
                                        extension_property_function_str,
                                    )(item, harvesting_vars)

                                else:
                                    self.logger_properties[
                                        "logger_level"
                                    ] = "ERROR"
                                    self.logger_properties[
                                        "logger_msg"
                                    ] = "Check your extension function name, second element of the tuple"
                                    logger.Logger(self.logger_properties)
                            else:
                                self.logger_properties[
                                    "logger_level"
                                ] = "ERROR"
                                self.logger_properties[
                                    "logger_msg"
                                ] = "Check your extension class name, second element of the tuple"
                                logger.Logger(self.logger_properties)
                        else:
                            extension_property_function_str = (
                                extension_property[1]
                            )
                            if hasattr(
                                imported_module,
                                extension_property_function_str,
                            ):
                                a = getattr(
                                    imported_module,
                                    extension_property_function_str,
                                )(item, harvesting_vars)
                                print(a)

                            else:
                                self.logger_properties[
                                    "logger_level"
                                ] = "ERROR"
                                self.logger_properties[
                                    "logger_msg"
                                ] = "Check your extension function name, second element of the tuple"
                                logger.Logger(self.logger_properties)
                        sys.path.remove(script_path_dir)
        # if (
        #     extension_properties is not None
        #     and extension_properties["item_scientific"] is True
        # ):
        #     scientific_class = scientific.Scientific()
        #     scientific_class.item(
        #         item, extension_properties["item_scientific"]
        #     )
        if extra_metadata is not None:
            if extra_metadata.get("extra_metadata"):
                ExtraMetadata(logger_properties=self.logger_properties).item(
                    item=item,
                    extra_metadata=extra_metadata,
                    harvesting_vars=harvesting_vars,
                )
            else:
                self.logger_properties["logger_level"] = "INFO"
                self.logger_properties[
                    "logger_msg"
                ] = "The `extra_metadata` is not activated. So, it does not add any extra metadata to the STAC item."
                # logger.Logger(self.logger_properties)

        # applying datacube extension to items

        if (
            extension_properties is not None
            and extension_properties["item_datacube"] is True
        ):
            datacube_class = datacube.Datacube()
            datacube_class.item_extension(
                item, harvesting_vars, logger_properties=self.logger_properties
            )

        # Because Collection does not provide point coordination, this condition was applied.
        # TODO: Should be checked by collection_footprint_point None ir not SHOULD BE REFACTORED .....
        if (
            harvesting_vars["collection_bbox"][0]
            == harvesting_vars["collection_bbox"][2]
            or harvesting_vars["collection_bbox"][1]
            == harvesting_vars["collection_bbox"][3]
        ):
            harvesting_vars["collection_bbox"] = [
                harvesting_vars["collection_bbox"][0] - constants.epilon,
                harvesting_vars["collection_bbox"][1] - constants.epilon,
                harvesting_vars["collection_bbox"][2] + constants.epilon,
                harvesting_vars["collection_bbox"][3] + constants.epilon,
            ]

        spatial_extent = pystac.SpatialExtent(
            bboxes=[harvesting_vars["collection_bbox"]]
        )
        temporal_extent = pystac.TemporalExtent(
            intervals=[harvesting_vars["collection_interval_time_final"]]
        )
        # An empty condition for either Temporal or Spatial extent
        # TODO: To be refactored
        if (
            harvesting_vars["collection_bbox"] is None
            or harvesting_vars["collection_interval_time_final"] is None
        ):
            spatial_extent = pystac.SpatialExtent(bboxes=[0.0, 0.0])
            temporal_extent = pystac.TemporalExtent(
                intervals=[[datetime.utcnow(), datetime.utcnow()]]
            )

        if (
            stac_existence_collection is True
            and collection_bbox_existed is not None
            and collection_interval_time_final_existed is not None
        ):
            if (
                spatial_extent.bboxes[0][0] != 0.0
                and spatial_extent.bboxes[0][1] != 0.0
            ):
                collection_boundingbox = utils.merge_bboxes(
                    collection_bbox_existed, harvesting_vars["collection_bbox"]
                )
                spatial_extent = pystac.SpatialExtent(
                    bboxes=[collection_boundingbox]
                )
            else:
                spatial_extent = pystac.SpatialExtent(
                    bboxes=[collection_bbox_existed]
                )
            if (
                temporal_extent.intervals[0][0] != datetime.utcnow()
                and temporal_extent.intervals[0][1] != datetime.utcnow()
            ):
                collection_interval_time_final = utils.merge_intervals(
                    collection_interval_time_final_existed,
                    harvesting_vars["collection_interval_time_final"],
                )
                temporal_extent = pystac.TemporalExtent(
                    intervals=[collection_interval_time_final]
                )
            else:
                temporal_extent = pystac.TemporalExtent(
                    intervals=[collection_interval_time_final_existed]
                )

        # final_collection: pystac.Collection = catalog.get_child(collection_id)  # type: ignore
        # print(len(list(catalog.get_children())))
        # print(len(list(final_collection.get_children())))
        # print("Before adding item to collection")

        if catalog.get_child(collection_id) is not None:
            catalog.get_child(collection_id).extent = pystac.Extent(  # type: ignore
                spatial=spatial_extent,
                temporal=temporal_extent,
            )

            catalog.get_child(collection_id).add_item(item)  # type: ignore
            item = None  # type: ignore

        return {"item": item}

    def SaveCatalog(
        self, catalog, catalog_dir, logger_properties: dict = dict()
    ):
        self.logger_properties = logger_properties
        try:
            catalog.normalize_hrefs(os.path.join(catalog_dir, "stac"))
            catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
            return True
        except Exception:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            if ex_type is not None and ex_value is not None:
                self.logger_properties["logger_level"] = "CRITICAL"
                self.logger_properties["logger_msg"] = (
                    "The Collection doesn't contain bounding box and/or temporal information. Therefore the STAC-Catalog cannot be created. Review the input values. %s : %s"
                    % (
                        ex_type.__name__,
                        ex_value,
                    )
                )
                logger.Logger(self.logger_properties)
            else:
                self.logger_properties["logger_level"] = "CRITICAL"
                self.logger_properties[
                    "logger_msg"
                ] = "The Collection doesn't contain bounding box and/or temporal information. Therefore the STAC-Catalog cannot be created. Review the input values."
                logger.Logger(self.logger_properties)
            return False
            # print(traceback.format_exc())
