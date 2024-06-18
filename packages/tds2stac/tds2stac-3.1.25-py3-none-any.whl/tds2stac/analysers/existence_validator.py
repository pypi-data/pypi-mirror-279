# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0

import os
from typing import Union

from ..logger import Logger


class ExistenceValidator(object):
    """
    A class for verifying the main STAC catalog's existence.
    This class is implemented in :class:`~tds2stac.STACCreator`.

    Args:
        stac_dir (st, Optional): Directory of the main STAC catalog (*)
        logger_properties (dict, optional): A dictionary of properties for logger. default is `None`.

    """

    stac_dir: str
    """
    Directory of the main STAC catalog. It can be a relative or absolute path.
    """
    logger_properties: Union[dict, None]
    """
    A dictionary of properties for logger. default is `None`.
    You can look at keys in :class:`~tds2stac.logger.Logger` class.
    """

    def __init__(
        self,
        stac_dir: str = os.getcwd(),
        logger_properties: Union[dict, None] = dict(),
    ):
        self.stac_dir = stac_dir
        self.stac_dir = os.path.join(self.stac_dir, "/catalog.json")
        if os.path.exists(self.stac_dir):
            self.existence = True
        else:
            self.existence = False
        if logger_properties is not None:
            logger_properties["logger_msg"] = self.existence
        Logger(logger_properties)

    def __repr__(self):
        return "<TDS2STACExistenceChecker existence: %s>" % (self.existence)
