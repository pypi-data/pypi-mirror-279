import json
import sys
from datetime import datetime

import pystac
import pytz

from ..logger import Logger

# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
from ..statics import constants


class ExtraMetadata:
    """
    A class to add extra metadata to the STAC items and collections.
    Args:
        logger_properties (dict): A dictionary containing the logger properties.
    """

    def __init__(self, logger_properties: dict = dict()):
        self.logger_properties = logger_properties

    def item(
        self,
        item: pystac.Item,
        extra_metadata: dict = dict(),
        harvesting_vars: dict = dict(),
    ):
        """
        Add extra metadata to the STAC item.
        """
        try:
            start_datetime = datetime.strptime(
                harvesting_vars["temporal_extent_start_datetime"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            ).replace(tzinfo=pytz.utc)
        except ValueError:
            start_datetime = datetime.strptime(
                harvesting_vars["temporal_extent_start_datetime"],
                "%Y-%m-%dT%H:%M:%SZ",
            ).replace(tzinfo=pytz.utc)
        try:
            end_datetime = datetime.strptime(
                harvesting_vars["temporal_extent_end_datetime"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            ).replace(tzinfo=pytz.utc)
        except ValueError:
            end_datetime = datetime.strptime(
                harvesting_vars["temporal_extent_end_datetime"],
                "%Y-%m-%dT%H:%M:%SZ",
            ).replace(tzinfo=pytz.utc)
        if extra_metadata.get("extra_metadata_file") is not None:
            extra_metadata_json = self.open_json_file(
                str(extra_metadata.get("extra_metadata_file"))
            )
            if (
                extra_metadata_json != {}
                and extra_metadata_json.get("item") is not None
            ):
                for key, value in extra_metadata_json["item"].items():
                    if key == "properties":
                        item.properties.update(value)
                    if key == "extra_fields":
                        item.extra_fields.update(value)
                    if key == "providers":
                        item.common_metadata.providers = value
                    if key == "license":
                        item.common_metadata.license = value
                    if key == "constellation":
                        item.common_metadata.constellation = value
                    if key == "platform":
                        item.common_metadata.platform = value
                    if key == "instruments":
                        item.common_metadata.instruments = value
                    if key == "gsd":
                        item.common_metadata.gsd = value
                    if key == "providers":
                        item.common_metadata.providers = value
                    if key == "title":
                        item.common_metadata.title = value
                    if key == "description":
                        item.common_metadata.description = value
                    if key == "start_datetime":
                        item.common_metadata.start_datetime = start_datetime
                    if key == "end_datetime":
                        item.common_metadata.end_datetime = end_datetime
                    if key == "updated":
                        item.common_metadata.updated = end_datetime
                    if key == "created":
                        item.common_metadata.created = start_datetime

            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "The `extra_metadata_file` is empty. So, the default extra metadata won't be added to the STAC item."
                Logger(self.logger_properties)
        else:
            self.logger_properties["logger_level"] = "WARNING"
            self.logger_properties[
                "logger_msg"
            ] = "The `extra_metadata_file` is not provided. So, the default extra metadata will be added to the STAC item."
            Logger(self.logger_properties)
            extra_metadata[
                "extra_metadata_file"
            ] = constants.default_extra_metadata_file
            extra_metadata_json = self.open_json_file(
                str(extra_metadata.get("extra_metadata_file"))
            )
            if (
                extra_metadata_json != {}
                and extra_metadata_json.get("item") is not None
            ):
                for key, value in extra_metadata_json["item"].items():
                    if key == "properties":
                        item.properties.update(value)
                    if key == "extra_fields":
                        item.extra_fields.update(value)
                    if key == "providers":
                        item.common_metadata.providers = value
                    if key == "license":
                        item.common_metadata.license = value
                    if key == "constellation":
                        item.common_metadata.constellation = value
                    if key == "platform":
                        item.common_metadata.platform = value
                    if key == "instruments":
                        item.common_metadata.instruments = value
                    if key == "gsd":
                        item.common_metadata.gsd = value
                    if key == "providers":
                        item.common_metadata.providers = value
                    if key == "title":
                        item.common_metadata.title = value
                    if key == "description":
                        item.common_metadata.description = value
                    if key == "start_datetime":
                        item.common_metadata.start_datetime = start_datetime
                    if key == "end_datetime":
                        item.common_metadata.end_datetime = end_datetime
                    if key == "updated":
                        item.common_metadata.updated = end_datetime
                    if key == "created":
                        item.common_metadata.created = start_datetime
            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "The default `extra_metadata_file` is empty. So, the default extra metadata won't be added to the STAC item."
                Logger(self.logger_properties)

    def collection(
        self, collection: pystac.Collection, extra_metadata: dict = dict()
    ):
        """
        Add extra metadata to the STAC collection.
        """
        if extra_metadata.get("extra_metadata_file") is not None:
            extra_metadata_json = self.open_json_file(
                str(extra_metadata.get("extra_metadata_file"))
            )
            if (
                extra_metadata_json != {}
                and extra_metadata_json.get("collection") is not None
            ):
                for key, value in extra_metadata_json["collection"].items():
                    if key == "extra_fields":
                        collection.extra_fields.update(value)
                    if key == "keywords":
                        collection.keywords = value
                    if key == "providers":
                        collection.providers = value
                    if key == "license":
                        collection.license = value
            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "The `extra_metadata_file` is empty. So, the default extra metadata won't be added to the STAC collection."
                Logger(self.logger_properties)
        else:
            self.logger_properties["logger_level"] = "WARNING"
            self.logger_properties[
                "logger_msg"
            ] = "The `extra_metadata_file` is not provided. So, the default extra metadata will be added to the STAC collection."
            Logger(self.logger_properties)
            extra_metadata[
                "extra_metadata_file"
            ] = constants.default_extra_metadata_file
            extra_metadata_json = self.open_json_file(
                str(extra_metadata.get("extra_metadata_file"))
            )
            if (
                extra_metadata_json != {}
                and extra_metadata_json.get("collection") is not None
            ):
                for key, value in extra_metadata_json["collection"].items():
                    if key == "extra_fields":
                        collection.extra_fields.update(value)
                    if key == "keywords":
                        collection.keywords = value
                    if key == "providers":
                        collection.providers = value
                    if key == "license":
                        collection.license = value
            else:
                self.logger_properties["logger_level"] = "WARNING"
                self.logger_properties[
                    "logger_msg"
                ] = "The default `extra_metadata_file` is empty. So, the default extra metadata won't be added to the STAC collection."
                Logger(self.logger_properties)

    def open_json_file(self, file_path: str) -> dict:
        """
        Open the JSON file.
        """
        try:
            loaded_json = json.load(open(file_path))
            return loaded_json

        except Exception:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            self.logger_properties["logger_level"] = "ERROR"
            if ex_type is not None and ex_value is not None:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not open {file_path}. %s: %s" % (
                    ex_type.__name__,
                    ex_value,
                )
            else:
                self.logger_properties[
                    "logger_msg"
                ] = f"Could not open {file_path}."
            Logger(self.logger_properties)
            return {}
