# -*- coding: utf-8 -*-

"""
implementation.
"""

import typing as T
import io
from pathlib import Path

from atomicwrites import atomic_write
from commentedconfigparser import CommentedConfigParser


def read_config_content(content: str) -> CommentedConfigParser:
    """
    Given the content of a config file, return the loaded config object.
    """
    config = CommentedConfigParser()
    config.optionxform = lambda option: option
    config.read_string(content)
    return config


def read_config_file(path) -> CommentedConfigParser:
    """
    Given a config file path, return the loaded config object.
    """
    return read_config_content(Path(path).read_text())


def _update_config(
    config: CommentedConfigParser,
    data: T.Dict[str, T.Dict[str, str]],
):
    """
    Surgically update config key value pair in a ``*.conf`` file.

    For example, the content of the ``worldserver.conf`` file is:

        [worldserver]
        RealmID = 1
        DataDir = "."

    The data is: {"worldserver": {"DataDir": "/home/azeroth-server/data"}}

    Then the return value is:

        [worldserver]
        RealmID = 1
        DataDir = "/home/azeroth-server/data"

    :param config: the loaded ``CommentedConfigParser``.
    :param data: python dictionary, the key value pair of the changes.
    """
    for section_name, section_data in data.items():
        for key, value in section_data.items():
            config[section_name][key] = str(value)


def update_config_content(
    content: str,
    data: T.Dict[str, T.Dict[str, str]],
) -> CommentedConfigParser:
    """
    Given the content of a config file, load the config object from it,
    apply changes, and return the config object.

    :param content: the string content of the ``*.conf`` file.
    :param data: python dictionary, the key value pair of the changes.
        The first key is the section name, the second key is the field name,
        and the value is the value.

    Example, let's say we want to change the ``DataDir`` field in the ``worldserver`` section
    from "." to "/home/azeroth-server/data".

    .. code-block::

        # content of the worldserver.conf file
        [worldserver]
        DataDir = "."

    .. code-block::

        update_config_content(
            content=content,
            data={"worldserver": {"DataDir": "/home/azeroth-server/data"}},
        )
    """
    config = read_config_content(content)
    _update_config(config, data)
    return config


def update_config_file(
    path,
    data: T.Dict[str, T.Dict[str, str]],
) -> CommentedConfigParser:
    """
    Given a config file path, load the config object from it,
    apply changes, and return the config object.

    It is the same as :func:`update_config_content`` but with a file path.
    """
    return update_config_content(Path(path).read_text(), data)


def write_config_content(config: CommentedConfigParser) -> str:
    """
    Write the config object to a string.
    """
    buffer = io.StringIO()
    config.write(buffer)
    return buffer.getvalue()


def write_config_file(config: CommentedConfigParser, path) -> Path:
    """
    Write the config object to a file.
    """
    content = write_config_content(config)
    p = Path(path)
    with atomic_write(f"{p}", overwrite=True) as f:
        f.write(content)
    return p


def apply_changes(
    path_input,
    path_output,
    data: T.Dict[str, T.Dict[str, str]],
) -> Path:
    """
    Given a config file path, load the config object from it,
    apply changes, and write to the target file, then return the target file path.

    :param path_input: the path of the input ``*.conf`` file. Can be str,
        or pathlib.Path, or pathlib_mate.Path.
    :param path_output: the path of the output ``*.conf`` file. Can be str,
        or pathlib.Path, or pathlib_mate.Path. **Note that the output file
        will be overwritten**.
    :param data: python dictionary, the key value pair of the changes.
        The first key is the section name, the second key is the field name,
        and the value is the value.

    :return: the path of the output file.

    See :func:`update_config_content` for more details about the update behavior.
    """
    config = update_config_file(path_input, data)
    return write_config_file(config, path_output)
