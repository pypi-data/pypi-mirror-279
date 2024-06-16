from typing import Any, Union
from os.path import join

"""
Copyright 2024 thiliapr

This file is part of TkJSONPath.
TkJSONPath is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
TkJSONPath is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with TkJSONPath. If not, see <https://www.gnu.org/licenses/>. 
"""

Key = Union[int, str]
Path = list[Key]
JSONObject = Union[list, dict]


def concat_path(path: str, obj_path: str) -> str:
    """
    Concat path.

    Args:
        path (str): A path.
        obj_path (str): Anthoer path.

    Returns:
        str: A path formed by joining two paths.
    """
    # Remove $
    obj_path = obj_path[1:]

    return path + obj_path


def get_safe_key(key: str) -> str:
    """
    Returns a safe key.

    Args:
        key (str): A string key.

    Returns:
        str: A path that can be safely used as a key.
    """
    return path.replace("\\", "\\\\").replace(".", "\\.").replace("[", "\\[")


def parse_path(path_str: str) -> Path:
    """
    Split the string path into a list of keys.

    Args:
        path_str (str): A string path.

    Returns:
        Path: A list of keys.
    """

    path: list[Key] = []

    skip_point = escape = index = False
    key = [""]

    def push():
        if key[0] == "":
            return

        if index:
            path.append(int(key[0]))
        else:
            path.append(key[0])
        key[0] = ""

    while path_str != "":
        # Read a char
        reading_char = path_str[0]
        path_str = path_str[1:]

        if escape:
            key[0] += reading_char
            escape = False
        elif reading_char == "\\":
            escape = True
        elif reading_char == "[":
            push()
            index = True
        elif reading_char == "]" and index:
            push()
            index = False
            skip_point = True
        elif reading_char == "." and (not skip_point):
            push()
        else:
            key[0] += reading_char

        if skip_point:
            skip_point = False

    # Append the last key to path
    push()

    # Remove $ from path
    path.pop(0)

    return path


def get(target: JSONObject, path: str | Path) -> Any:
    """
    Get the value specified by path from target.

    Args:
        target (JSONObject): A json object.
        path (Union[str, Path]): The specified path.

    Returns:
        Any: The value specified by path from target.
    """
    if isinstance(path, str):
        path = parse_path(path)

    for cur_key in path:
        target = target[cur_key]

    return target


def assign(target: JSONObject, path: str | Path, value: Any) -> Any:
    """
    Assign a value to path in `target`.

    Args:
        target (JSONObject): A json object.
        path (Union[str, Path]): The specified path.
        value (Any): The assigned value.

    Returns:
        Any: The assigned value.
    """
    if isinstance(path, str):
        path = parse_path(path)

    get(target, path[:-1])[path[-1]] = value

    return value
