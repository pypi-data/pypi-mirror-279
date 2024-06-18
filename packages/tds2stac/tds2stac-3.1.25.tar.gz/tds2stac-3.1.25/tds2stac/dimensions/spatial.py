# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0


from shapely import geometry


class Spatial(object):
    def regulator(self, main_dict, spatial_information):
        """A function for regulating the spatial information of a catalog"""
        # TODO: make a function to to the same procedure once for all

        errors = []
        if (
            main_dict["horizontal_extent_lon_min"] is not None
            and not main_dict.get("horizontal_extent_lon_min").isspace()
        ) and spatial_information is None:
            main_dict["horizontal_extent_lon_min"] = main_dict[
                "horizontal_extent_lon_min"
            ].replace(",", ".")
        elif (
            (
                main_dict["horizontal_extent_lon_min"] is None
                or main_dict.get("horizontal_extent_lon_min").isspace()
            )
            or main_dict["horizontal_extent_lon_min"] is not None
        ) and spatial_information is not None:
            if len(spatial_information) == 4:
                main_dict["horizontal_extent_lon_min"] = str(
                    spatial_information[0]
                )
            elif len(spatial_information) == 2:
                main_dict["horizontal_extent_lon_min"] = str(
                    spatial_information[0]
                )
            else:
                errors.append(
                    "There are inaccuracies in the `spatial_information` input values. Please include [horizontal_extent_lon_min, horizontal_extent_lon_max, horizontal_extent_lat_min, horizontal_extent_lat_max] or [long, lat] in the `spatial_information` attr, depending on the data's dimensions"
                )
        elif (
            main_dict["horizontal_extent_lon_min"] is None
            or main_dict.get("horizontal_extent_lon_min").isspace()
        ) and spatial_information is None:
            errors.append(
                "Minimum Longitude is None in the given dataset. Please review your `tag_config.json` file or use `spatial_information` attr to add the spatial coordinate and harvest again."
            )

        if (
            main_dict["horizontal_extent_lon_max"] is not None
            and spatial_information is None
        ):
            main_dict["horizontal_extent_lon_max"] = main_dict[
                "horizontal_extent_lon_max"
            ].replace(",", ".")
        elif (
            main_dict["horizontal_extent_lon_max"] is None
            or main_dict["horizontal_extent_lon_max"] is not None
        ) and spatial_information is not None:
            if len(spatial_information) == 4:
                main_dict["horizontal_extent_lon_max"] = str(
                    spatial_information[1]
                )
            elif len(spatial_information) == 2:
                main_dict["horizontal_extent_lon_max"] = str(
                    spatial_information[0]
                )
            else:
                errors.append(
                    "There are inaccuracies in the `spatial_information` input values. Please include [horizontal_extent_lon_min, horizontal_extent_lon_max, horizontal_extent_lat_min, horizontal_extent_lat_max] or [long, lat] in the `spatial_information` attr, depending on the data's dimensions"
                )
        elif (
            main_dict["horizontal_extent_lon_max"] is None
            or main_dict.get("horizontal_extent_lon_max").isspace()
        ) and spatial_information is None:
            errors.append(
                "Maximum Longitude is None in the given dataset. Please review your `tag_config.json` file or use `spatial_information` attr to add the spatial coordinate and harvest again."
            )

        if (
            main_dict["horizontal_extent_lat_min"] is not None
            and spatial_information is None
        ):
            main_dict["horizontal_extent_lat_min"] = main_dict[
                "horizontal_extent_lat_min"
            ].replace(",", ".")
        elif (
            main_dict["horizontal_extent_lat_min"] is None
            or main_dict["horizontal_extent_lat_min"] is not None
        ) and spatial_information is not None:
            if len(spatial_information) == 4:
                main_dict["horizontal_extent_lat_min"] = str(
                    spatial_information[2]
                )
            elif len(spatial_information) == 2:
                main_dict["horizontal_extent_lat_min"] = str(
                    spatial_information[1]
                )
            else:
                errors.append(
                    "There are inaccuracies in the `spatial_information` input values. Please include [horizontal_extent_lon_min, horizontal_extent_lon_max, horizontal_extent_lat_min, horizontal_extent_lat_max] or [long, lat] in the `spatial_information` attr, depending on the data's dimensions"
                )
        elif (
            main_dict["horizontal_extent_lat_min"] is None
            or main_dict.get("horizontal_extent_lat_min").isspace()
        ) and spatial_information is None:
            errors.append(
                "Minimum Latitude is None in the given dataset. Please review your `tag_config.json` file or use `spatial_information` attr to add the spatial coordinate and harvest again."
            )

        if (
            main_dict["horizontal_extent_lat_max"] is not None
            and spatial_information is None
        ):
            main_dict["horizontal_extent_lat_max"] = main_dict[
                "horizontal_extent_lat_max"
            ].replace(",", ".")
        elif (
            main_dict["horizontal_extent_lat_max"] is None
            or main_dict["horizontal_extent_lat_max"] is not None
        ) and spatial_information is not None:
            if len(spatial_information) == 4:
                main_dict["horizontal_extent_lat_max"] = str(
                    spatial_information[3]
                )
            elif len(spatial_information) == 2:
                main_dict["horizontal_extent_lat_max"] = str(
                    spatial_information[1]
                )
            else:
                errors.append(
                    "There are inaccuracies in the `spatial_information` input values. Please include [horizontal_extent_lon_min, horizontal_extent_lon_max, horizontal_extent_lat_min, horizontal_extent_lat_max] or [long, lat] in the `spatial_information` attr, depending on the data's dimensions"
                )
        elif (
            main_dict["horizontal_extent_lat_max"] is None
            or main_dict.get("horizontal_extent_lat_max").isspace()
        ) and spatial_information is None:
            errors.append(
                "Maximum Latitude is None in the given dataset. Please review your `tag_config.json` file or use `spatial_information` attr to add the spatial coordinate and harvest again."
            )
        if errors == []:
            # A condition for longitudes more than 180 e.g. 360 degree. Cause STAC doesn't support longs
            # more than 180
            if (
                float(main_dict["horizontal_extent_lon_min"]) > 180
                or float(main_dict["horizontal_extent_lon_max"]) > 180
            ):
                main_dict["horizontal_extent_lon_min"] = str(
                    float(main_dict["horizontal_extent_lon_min"]) - 180
                )
                main_dict["horizontal_extent_lon_max"] = str(
                    float(main_dict["horizontal_extent_lon_max"]) - 180
                )
            return (
                main_dict["horizontal_extent_lon_min"],
                main_dict["horizontal_extent_lon_max"],
                main_dict["horizontal_extent_lat_min"],
                main_dict["horizontal_extent_lat_max"],
            )
        else:
            return errors

    def harvester(self, main_dict, linestring=None):
        # TODO: for making the foorprint we have to check another attribute for making PolyLINE and PolyGON with more than boxes points
        if (
            main_dict["horizontal_extent_lon_min"]
            == main_dict["horizontal_extent_lon_max"]
            or main_dict["horizontal_extent_lat_max"]
            == main_dict["horizontal_extent_lat_min"]
        ):
            boundingBox = [
                main_dict["horizontal_extent_lon_min"],
                main_dict["horizontal_extent_lat_max"],
            ]
            main_dict["item_bbox"] = list(map(float, boundingBox))
            main_dict["item_footprint"] = geometry.Point(
                main_dict["item_bbox"][0],
                main_dict["item_bbox"][1],
            )

            if main_dict["collection_footprint_point"] is None:
                main_dict["collection_footprint_point"] = main_dict[
                    "item_footprint"
                ]
            main_dict["collection_footprint_point"] = geometry.shape(
                main_dict["item_footprint"]
            ).union(geometry.shape(main_dict["collection_footprint_point"]))
            main_dict["collection_bbox"] = list(
                main_dict["collection_footprint_point"].bounds
            )

        elif linestring is True:
            boundingBox = [
                main_dict["horizontal_extent_lon_min"],
                main_dict["horizontal_extent_lat_min"],
                main_dict["horizontal_extent_lon_max"],
                main_dict["horizontal_extent_lat_max"],
            ]
            main_dict["item_bbox"] = list(map(float, boundingBox))

            main_dict["item_footprint"] = geometry.LineString(
                [
                    [main_dict["item_bbox"][0], main_dict["item_bbox"][1]],
                    [main_dict["item_bbox"][2], main_dict["item_bbox"][3]],
                ]
            )

            if (
                main_dict["collection_bbox"] is None
                or main_dict["collection_bbox"] == []
            ):
                main_dict["collection_bbox"] = main_dict["item_bbox"]
            else:
                main_dict["collection_bbox"] = [
                    min(
                        main_dict["collection_bbox"][0],
                        main_dict["item_bbox"][0],
                    ),
                    min(
                        main_dict["collection_bbox"][1],
                        main_dict["item_bbox"][1],
                    ),
                    max(
                        main_dict["collection_bbox"][2],
                        main_dict["item_bbox"][2],
                    ),
                    max(
                        main_dict["collection_bbox"][3],
                        main_dict["item_bbox"][3],
                    ),
                ]

        else:
            # TODO: we have to add another feature for LineString and Polygon
            boundingBox = [
                main_dict["horizontal_extent_lon_min"],
                main_dict["horizontal_extent_lat_min"],
                main_dict["horizontal_extent_lon_max"],
                main_dict["horizontal_extent_lat_max"],
            ]
            main_dict["item_bbox"] = list(map(float, boundingBox))
            main_dict["item_footprint"] = geometry.Polygon(
                [
                    [main_dict["item_bbox"][0], main_dict["item_bbox"][1]],
                    [main_dict["item_bbox"][0], main_dict["item_bbox"][3]],
                    [main_dict["item_bbox"][2], main_dict["item_bbox"][3]],
                    [main_dict["item_bbox"][2], main_dict["item_bbox"][1]],
                ]
            )
            if (
                main_dict["collection_bbox"] is None
                or main_dict["collection_bbox"] == []
            ):
                main_dict["collection_bbox"] = main_dict["item_bbox"]
            else:
                main_dict["collection_bbox"] = [
                    min(
                        main_dict["collection_bbox"][0],
                        main_dict["item_bbox"][0],
                    ),
                    min(
                        main_dict["collection_bbox"][1],
                        main_dict["item_bbox"][1],
                    ),
                    max(
                        main_dict["collection_bbox"][2],
                        main_dict["item_bbox"][2],
                    ),
                    max(
                        main_dict["collection_bbox"][3],
                        main_dict["item_bbox"][3],
                    ),
                ]
