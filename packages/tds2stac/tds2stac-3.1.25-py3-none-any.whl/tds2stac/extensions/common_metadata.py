# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
from datetime import datetime

import pytz

from ..logger import Logger


class CommonMetadata:
    def item(self, item, harvesting_vars, logger_properties: dict = dict()):
        # Add auxiliary information to items
        if harvesting_vars.get("temporal_extent_start_datetime") is not None:
            try:
                item.common_metadata.start_datetime = datetime.strptime(
                    harvesting_vars["temporal_extent_start_datetime"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                ).replace(tzinfo=pytz.utc)
            except ValueError:
                try:
                    item.common_metadata.start_datetime = datetime.strptime(
                        harvesting_vars["temporal_extent_start_datetime"],
                        "%Y-%m-%dT%H:%M:%SZ",
                    ).replace(tzinfo=pytz.utc)
                except ValueError:
                    logger_properties["logger_level"] = "WARNING"
                    logger_properties[
                        "logger_msg"
                    ] = "Start datetime is in an unknown format."
                    Logger(logger_properties)
        if harvesting_vars.get("temporal_extent_end_datetime") is not None:
            try:
                item.common_metadata.end_datetime = datetime.strptime(
                    harvesting_vars["temporal_extent_end_datetime"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                ).replace(tzinfo=pytz.utc)
            except ValueError:
                try:
                    item.common_metadata.end_datetime = datetime.strptime(
                        harvesting_vars["temporal_extent_end_datetime"],
                        "%Y-%m-%dT%H:%M:%SZ",
                    ).replace(tzinfo=pytz.utc)
                except ValueError:
                    logger_properties["logger_level"] = "WARNING"
                    logger_properties[
                        "logger_msg"
                    ] = "End datetime is in an unknown format."
                    Logger(logger_properties)
        if (
            harvesting_vars["description"] is not None
            and harvesting_vars["service_url_html"] is not None
        ):
            item.common_metadata.description = (
                harvesting_vars["description"]
                + "\n\n [Link to the data catalog in TDS]("
                + harvesting_vars["service_url_html"]
                + ")"
            )
        if harvesting_vars.get("constellation") is not None:
            item.common_metadata.constellation = harvesting_vars[
                "constellation"
            ]
        if harvesting_vars.get("gsd") is not None:
            item.common_metadata.gsd = harvesting_vars["gsd"]
        if harvesting_vars.get("instruments") is not None:
            item.common_metadata.instruments = harvesting_vars["instruments"]
        if harvesting_vars.get("license") is not None:
            item.common_metadata.license = harvesting_vars["license"]
        if harvesting_vars.get("mission") is not None:
            item.common_metadata.mission = harvesting_vars["mission"]
        if harvesting_vars.get("providers") is not None:
            item.common_metadata.providers = harvesting_vars["providers"]
        if harvesting_vars.get("title") is not None:
            item.common_metadata.title = harvesting_vars["title"]
        if harvesting_vars.get("updated") is not None:
            item.common_metadata.updated = harvesting_vars["updated"]
        if harvesting_vars.get("created") is not None:
            item.common_metadata.created = harvesting_vars["created"]
