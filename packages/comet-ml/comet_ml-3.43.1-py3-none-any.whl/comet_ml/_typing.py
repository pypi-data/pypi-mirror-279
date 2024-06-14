# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************

"""

This module contains useful types and mirror the typing module

"""

# isort: off

from typing import *  # noqa
from typing import (
    IO,
    BinaryIO,
    Union,
    Tuple,
    Dict,
    Any,
    Callable,
    List,
    Optional,
    NamedTuple,
)  # noqa


class ValidFilePath(str):
    """This type help marking a file_path as existing on disk as checked by `is_valid_file_path`"""

    pass


class TemporaryFilePath(ValidFilePath):
    """This type help marking a file_path as valid on disk as checked by `is_valid_file_path`"""

    pass


class BackendFeatureSupportByVersion(NamedTuple):
    """This type encapsulates info about result of minimum backend version check for support of specific feature"""

    feature_supported: bool
    min_backend_version_supported: str


class ColorWithShadesMap(NamedTuple):
    """This type encapsulates info about color map for panel"""

    primary: str
    light: str


UserText = Union[bytes, Text]  # noqa
MemoryUploadable = Union[IO, UserText]  # noqa
# With typing_extensions, we could use Literal["all"]
TensorflowInput = Union[int, str]  # noqa
Number = Union[int, float]

HeartBeatResponse = Tuple[int, Dict[str, Any], bool]
Point3D = Union[List[float], Tuple[float, float, float]]
OnMessageSentCallback = Callable[[int, bool, bool, Optional[str]], None]
OnMessagesBatchSentCallback = Callable[[List[int], bool, bool, Optional[str]], None]
PanelColorMap = Dict[str, ColorWithShadesMap]
