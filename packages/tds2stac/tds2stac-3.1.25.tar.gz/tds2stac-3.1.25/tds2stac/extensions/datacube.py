# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0


from pystac.extensions.datacube import (
    DatacubeExtension,
    Dimension,
    DimensionType,
    Variable,
    VariableType,
)

from ..logger import Logger


class Datacube(object):
    """
    This class is responsible for adding the datacube extension to the STAC Item.
    Args:
        item (pystac.Item): The STAC Item to be extended.
        harvesting_vars (dict): The dictionary of the variables and dimensions of the dataset.
        logger_properties (dict): The dictionary of the logger properties.
    """

    def item_extension(
        self, item, harvesting_vars, logger_properties: dict = dict()
    ):
        self.logger_properties = logger_properties
        variables = (
            {}
        )  # variables dictionary for gathering the Variable objects
        dimensions = (
            {}
        )  # dimensions dictionary for gathering the Dimension objects
        cube = DatacubeExtension.ext(item, add_if_missing=True)
        if harvesting_vars.get("variable_dimensions") is not None:
            variable_dimensions = [
                elem.replace(" ", ",").split(",") if " " in elem else [elem]
                for elem in harvesting_vars["variable_dimensions"]
            ]
        else:
            self.logger_properties["logger_level"] = "WARNING"
            self.logger_properties[
                "logger_msg"
            ] = "The variable's dimensions list is not involved in the output dictionary. Check your dataset in Thredds or correct keys in your `tag_config.json` file to produce new lists. Datacube extension is not added to the STAC Item."
            Logger(self.logger_properties)
            return
        if len(harvesting_vars["variable_ids"]) != len(variable_dimensions):
            # Another solution for this is to index each output element and find the None values to decide about them later
            if harvesting_vars["variable_ids"] is None:
                harvesting_vars["variable_ids"] = []
            self.logger_properties["logger_level"] = "WARNING"
            self.logger_properties[
                "logger_msg"
            ] = "The length of the variable's IDs list and the variable's dimensions list are not equal. Check your dataset in Thredds or correct keys in your `tag_config.json` file to produce new lists. Datacube extension is not added to the STAC Item."
            Logger(self.logger_properties)
            return
        else:
            for i, v in enumerate(harvesting_vars["variable_ids"]):
                variable_dict = dict()
                variable_dict["dimensions"] = variable_dimensions[i]
                variable_dict["type"] = VariableType.DATA.value
                if (
                    harvesting_vars["variable_description"] is not None
                    and len(harvesting_vars["variable_ids"])
                    == len(harvesting_vars["variable_description"])
                    and len(harvesting_vars["variable_description"])
                    != harvesting_vars["variable_description"].count(None)
                ):
                    if harvesting_vars["variable_description"][i] is not None:
                        variable_dict["description"] = harvesting_vars[
                            "variable_description"
                        ][i]
                variable_dict["dimensions"] = variable_dimensions[i]
                if (
                    harvesting_vars["variable_unit"] is not None
                    and len(harvesting_vars["variable_unit"])
                    == len(variable_dimensions)
                    and len(harvesting_vars["variable_unit"])
                    != harvesting_vars["variable_unit"].count(None)
                ):
                    if harvesting_vars["variable_unit"][i] is not None:
                        variable_dict["units"] = harvesting_vars[
                            "variable_unit"
                        ][i]
                variables[harvesting_vars["variable_ids"][i]] = Variable(
                    variable_dict
                )

        # Horizontal Spatial Dimension
        list_of_required_keys = [
            "horizontal_ids_lat",
            "horizontal_ids_lon",
            "horizontal_axis_x",
            "horizontal_axis_y",
            "horizontal_extent_lon_min",
            "horizontal_extent_lon_max",
            "horizontal_extent_lat_min",
            "horizontal_extent_lat_max",
        ]

        if all(
            harvesting_vars.get(key) is not None
            for key in list_of_required_keys
        ):
            horizontal_dict = dict()
            horizontal_dict = {
                "type": DimensionType.SPATIAL.value,
                "axis": harvesting_vars["horizontal_axis_x"],
                "description": harvesting_vars["horizontal_description_lon"],
                "extent": [
                    float(
                        harvesting_vars["horizontal_extent_lon_min"].replace(
                            ",", "."
                        )
                    ),
                    float(
                        harvesting_vars["horizontal_extent_lon_max"].replace(
                            ",", "."
                        )
                    ),
                ],
                "reference_system": harvesting_vars[
                    "horizontal_reference_system"
                ],
            }
            dimensions[harvesting_vars["horizontal_ids_lon"]] = Dimension(
                horizontal_dict
            )
            horizontal_dict = dict()
            horizontal_dict = {
                "type": DimensionType.SPATIAL.value,
                "axis": harvesting_vars["horizontal_axis_y"],
                "description": harvesting_vars["horizontal_description_lat"],
                "extent": [
                    float(
                        harvesting_vars["horizontal_extent_lat_min"].replace(
                            ",", "."
                        )
                    ),
                    float(
                        harvesting_vars["horizontal_extent_lat_max"].replace(
                            ",", "."
                        )
                    ),
                ],
                "reference_system": harvesting_vars[
                    "horizontal_reference_system"
                ],
            }
            dimensions[harvesting_vars["horizontal_ids_lat"]] = Dimension(
                horizontal_dict
            )
        else:
            logger_string_output = ""
            logger_properties["logger_level"] = "WARNING"
            for key in list_of_required_keys:
                if harvesting_vars.get(key) is None:
                    logger_string_output = (
                        logger_string_output
                        + f"{key}: {harvesting_vars.get(key)} \n"
                    )
            logger_properties[
                "logger_msg"
            ] = f"Required horizontal attributes aren't involved in the output dictionary. Check your dataset in Thredds or check the following lists and reconfig your `tag_config.json` file. {logger_string_output}"
            Logger(logger_properties)
            return

        # Vertical Spatial Dimension
        list_of_required_keys = [
            "vertical_id",
            "vertical_axis",
            "vertical_extent_upper",
            "vertical_extent_lower",
        ]
        if all(
            harvesting_vars.get(key) is not None and harvesting_vars[key] != []
            for key in list_of_required_keys
        ):
            vertical_dict = dict()
            vertical_dict = {
                "type": DimensionType.SPATIAL.value,
                "axis": harvesting_vars["vertical_axis"],
                "description": harvesting_vars["vertical_description"],
                "extent": [
                    float(
                        harvesting_vars["vertical_extent_lower"].replace(
                            ",", "."
                        )
                    ),
                    float(
                        harvesting_vars["vertical_extent_upper"].replace(
                            ",", "."
                        )
                    ),
                ],
            }
            dimensions[harvesting_vars["vertical_id"]] = Dimension(
                vertical_dict
            )
        else:
            logger_string_output = ""
            # logger_properties["logger_level"] = "WARNING"
            for key in list_of_required_keys:
                if harvesting_vars.get(key) is None:
                    logger_string_output = (
                        logger_string_output
                        + f"{key}: {harvesting_vars.get(key)} \n"
                    )
            # logger_properties[
            #    "logger_msg"
            # ] = f"Required vertical attributes aren't involved in the output dictionary. Check your dataset in Thredds or check the following lists and reconfig your `tag_config.json` file. {logger_string_output}"
            # Logger(logger_properties)

        # Temporal Dimension
        list_of_required_keys = [
            "temporal_id",
            "temporal_extent_start_datetime",
            "temporal_extent_end_datetime",
        ]
        if all(
            harvesting_vars.get(key) is not None
            for key in list_of_required_keys
        ):
            temporal_dict = dict()
            temporal_dict = {
                "type": DimensionType.TEMPORAL.value,
                "description": harvesting_vars["temporal_description"],
                "extent": [
                    harvesting_vars["temporal_extent_start_datetime"],
                    harvesting_vars["temporal_extent_end_datetime"],
                ],
            }
            dimensions[harvesting_vars["temporal_id"]] = Dimension(
                temporal_dict
            )
        else:
            logger_string_output = ""
            logger_properties["logger_level"] = "WARNING"
            for key in list_of_required_keys:
                if harvesting_vars.get(key) is None:
                    logger_string_output = (
                        logger_string_output
                        + f"{key}: {harvesting_vars.get(key)} \n"
                    )

            logger_properties[
                "logger_msg"
            ] = f"Required attributes aren't involved in the output dictionary. Check your dataset in Thredds or check the following lists and reconfig your `tag_config.json` file. \n{logger_string_output}"
            Logger(logger_properties)
            return

        # Additional Dimensions
        anotherlist = [
            "x",
            "y",
            "time",
            "longitude",
            "latitude",
            "t",
            "z",
            "height",
        ]
        for id in harvesting_vars["additional_ids"]:
            if id.lower() not in [
                i.lower() for i in list(dimensions.keys()) + anotherlist
            ]:
                additional_dict = dict()
                additional_dict = {
                    "type": harvesting_vars["additional_type"],
                    "extent": [None, None],
                }
                dimensions[id] = Dimension(additional_dict)
        cube.apply(dimensions=dimensions, variables=variables)
