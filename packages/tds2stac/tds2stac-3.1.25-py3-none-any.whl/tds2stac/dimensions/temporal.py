from datetime import datetime

# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
import pytz


class Temporal(object):
    def regulator(self, main_dict, temporal_format_by_dataname, data_name):
        errors = []
        warnings = []

        if temporal_format_by_dataname is not None:
            try:
                main_dict[
                    "temporal_extent_start_datetime"
                ] = datetime.strptime(
                    str(data_name), temporal_format_by_dataname
                ).strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                )

            except Exception as e:
                start_datetime = self.safe_strip(
                    main_dict.get("temporal_extent_start_datetime")
                )
                if start_datetime:
                    main_dict[
                        "temporal_extent_start_datetime"
                    ] = start_datetime
                    warnings.append(
                        f"There is a problem with `temporal_format_by_dataname`. Revise your input. {e.__class__.__name__} : {e}"
                    )
                else:
                    errors.append(
                        f"Start DateTime is None or empty in the given dataset. Please review your `tag_config.json` file. {e.__class__.__name__} : {e}"
                    )

        else:
            start_datetime = self.safe_strip(
                main_dict.get("temporal_extent_start_datetime")
            )
            if start_datetime:
                main_dict["temporal_extent_start_datetime"] = start_datetime
            else:
                errors.append(
                    "Start DateTime is None or empty in the given dataset. Please review your `tag_config.json` file."
                )

        if temporal_format_by_dataname is not None:
            try:
                main_dict["temporal_extent_end_datetime"] = datetime.strptime(
                    str(data_name), temporal_format_by_dataname
                ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            except Exception as e:
                end_datetime = self.safe_strip(
                    main_dict.get("temporal_extent_end_datetime")
                )
                if end_datetime:
                    main_dict["temporal_extent_end_datetime"] = end_datetime
                    warnings.append(
                        f"There is a problem with `temporal_format_by_dataname`. Revise your input. {e.__class__.__name__} : {e}"
                    )
                else:
                    errors.append(
                        f"End DateTime is None or empty in the given dataset. Please review your `tag_config.json` file. {e.__class__.__name__} : {e}"
                    )

        else:
            end_datetime = self.safe_strip(
                main_dict.get("temporal_extent_end_datetime")
            )
            if end_datetime:
                main_dict["temporal_extent_end_datetime"] = end_datetime
            else:
                errors.append(
                    "End DateTime is None or empty in the given dataset. Please review your `tag_config.json` file."
                )

        # Check if both start and end date-times are present and not just whitespace
        if all(
            main_dict.get(key) and not main_dict.get(key).isspace()
            for key in [
                "temporal_extent_start_datetime",
                "temporal_extent_end_datetime",
            ]
        ):
            # Parse and append start and end date-times to collection_interval_time
            main_dict["collection_interval_time"].extend(
                [
                    self.parse_datetime_with_fallback(
                        main_dict["temporal_extent_start_datetime"],
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                        "%Y-%m-%dT%H:%M:%SZ",
                        pytz.utc,
                    ),
                    self.parse_datetime_with_fallback(
                        main_dict["temporal_extent_end_datetime"],
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                        "%Y-%m-%dT%H:%M:%SZ",
                        pytz.utc,
                    ),
                ]
            )
            # Sort the collection_interval_time list
            main_dict["collection_interval_time"].sort()
        else:
            # Append error if either start or end datetime is missing or only whitespace
            errors.append(
                "Start or End DateTime is None or empty in the given dataset. Please review your `tag_config.json` file."
            )

        if errors != [] and warnings != []:
            return errors, warnings
        elif errors != [] and warnings == []:
            return errors, None
        elif errors == [] and warnings != []:
            return None, warnings
        else:
            return None, None

    # Function to parse datetime with a fallback format
    def parse_datetime_with_fallback(
        self, datetime_str, primary_format, fallback_format, tzinfo
    ):
        try:
            return datetime.strptime(datetime_str, primary_format).replace(
                tzinfo=tzinfo
            )
        except ValueError:
            return datetime.strptime(datetime_str, fallback_format).replace(
                tzinfo=tzinfo
            )

    def safe_strip(self, value):
        return value.strip() if value is not None else ""
