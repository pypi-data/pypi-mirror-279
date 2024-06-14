# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2023 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
from typing import Any, List, Optional, Tuple, Union

from .parameter import Parameter


def validate_type_str(value: Any, allow_empty: bool = True) -> bool:
    valid = validate_type(value, (str,), allow_empty=allow_empty)
    if not valid:
        return False

    if not allow_empty:
        return value != ""

    return True


def validate_type_int(value: Any, allow_empty: bool = True) -> bool:
    return validate_type(value, (int,), allow_empty=allow_empty)


def validate_type_float(value: Any, allow_empty: bool = True) -> bool:
    return validate_type(value, (float,), allow_empty=allow_empty)


def validate_type_numeric(value: Any, allow_empty: bool = True) -> bool:
    return validate_type(value, (float, int), allow_empty=allow_empty)


def validate_type_bool(value: Any, allow_empty: bool = True) -> bool:
    return validate_type(value, (bool,), allow_empty=allow_empty)


def validate_type_list(value: Any, allow_empty: bool = True) -> bool:
    return validate_type(value, (list,), allow_empty=allow_empty)


def validate_type_list_of_numbers(value: List[Any]) -> bool:
    if not validate_type_list(value, allow_empty=False):
        return False
    res = [validate_type_numeric(n, allow_empty=False) for n in value]
    return all(res)


def validate_type_dict(value: Any, allow_empty: bool = True) -> bool:
    return validate_type(value, (dict,), allow_empty=allow_empty)


def validate_type(value: Any, types: Tuple, allow_empty: bool) -> bool:
    if value is None:
        return allow_empty

    return any(isinstance(value, t) for t in types)


def validate_possible_values(
    value: Any, possible_values: Optional[List], allow_empty: bool
) -> bool:
    if value is None:
        return allow_empty

    return value in possible_values


def validate_parameter(parameter: Parameter) -> Tuple[bool, Optional[str]]:
    valid_value = (
        validate_possible_values(
            value=parameter.value,
            possible_values=parameter.possible_values,
            allow_empty=parameter.allow_empty,
        )
        if parameter.possible_values is not None
        else True
    )

    if not valid_value:
        possible_values_str = [str(v) for v in parameter.possible_values]

        if parameter.allow_empty:
            msg = "parameter %r must be one of [%s] or None but %r was given" % (
                parameter.name,
                ", ".join(possible_values_str),
                parameter.value,
            )
        else:
            msg = "parameter %r must be one of [%s] but %r was given" % (
                parameter.name,
                ", ".join(possible_values_str),
                parameter.value,
            )
        return False, msg

    valid_type = validate_type(
        value=parameter.value, types=parameter.types, allow_empty=parameter.allow_empty
    )

    if not valid_type:
        param_type = None if parameter.value is None else type(parameter.value).__name__

        if parameter.allow_empty:
            msg = "parameter %r must be of type(s) %r or None but %r was given" % (
                parameter.name,
                types_list(parameter.types),
                param_type,
            )
        else:
            msg = "parameter %r must be of type(s) %r but %r was given" % (
                parameter.name,
                types_list(parameter.types),
                param_type,
            )
        return False, msg

    return True, None


def types_list(types: Union[Tuple, List]) -> Union[str, List[str]]:
    type_names = []
    for t in types:
        type_names.append(t.__name__)

    if len(type_names) > 1:
        return type_names
    elif len(type_names) == 1:
        return type_names[0]
    else:
        return []


def flatten_list(xss: List[List[Any]]):
    return [x for xs in xss for x in xs]
