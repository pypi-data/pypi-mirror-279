# Copyright © 2024 pkeorley
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.

import json
import typing as t


T = t.TypeVar("T")


def deserialize(value: t.Optional[str], type: t.Type[T]) -> T:
    if value is None:
        return None

    elif type == int:
        return int(value)

    elif type == str:
        return str(value)

    elif type == list:
        if not value.startswith("["):
            raise ValueError("Provided value is not a list")
        return json.loads(value)

    raise TypeError(f"Type {type} not supported")
