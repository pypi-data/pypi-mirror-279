# -*- coding: utf-8 -*-

"""Module for configurations"""
from __future__ import annotations

import glob
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import yaml
from iris.cube import CubeList
from iris.fileformats.netcdf import CF_CONVENTIONS_VERSION
from iris.util import equalise_attributes
import uuid

from gordias import __version__

logger = logging.getLogger(__name__)


@dataclass
class InputTransferConfiguration:
    """Input attribute configuration."""

    attr_name: str
    attributes: list[str]


@dataclass
class OutputCreateConfiguration:
    """Output attribute configuration."""

    attr_name: str
    attribute: str


@dataclass
class GlobalAttributesInputConfiguration:
    """Configuration for global input attributes."""

    default: str | None = None
    drop: list[str] | None = None
    transfer: list[InputTransferConfiguration] | None = None


@dataclass
class GlobalAttributesOutputConfiguration:
    """Configuration for global output attributes."""

    create: list[OutputCreateConfiguration] | None = None


@dataclass
class GlobalAttributesConfiguration:
    """Configuration for global attributes."""

    input: GlobalAttributesInputConfiguration
    output: GlobalAttributesOutputConfiguration
    extra_attributes: dict | None = None


def _get_default_configuration_path() -> list[str]:
    """Return the path of the default YAML configuration file."""
    directory = os.path.join(os.path.dirname(__file__), "etc")
    if os.path.isdir(directory):
        return glob.glob(os.path.join(directory, "*.yml"))
    else:
        raise RuntimeError(
            "Failed to find YAML configuration file in directory " f"<{directory}>."
        )


def _get_default_configuration_metadata(path: str) -> dict:
    """Return the default configuration metadata."""
    try:
        with open(path, "r") as f:
            config_file = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise yaml.YAMLError(f"Error in configuration file: {exc}") from exc
    return config_file


def _get_default_configuration() -> dict:
    """Return the metadata of the default configuration."""
    config = {}
    for path in _get_default_configuration_path():
        logger.info(f"Reading configuration default definitions from file {path}")
        config_file = _get_default_configuration_metadata(path)
        try:
            config = config_file.get("config", None)
            config.update(get_configuration(config))
        except ValueError:
            raise ValueError(
                f"Failed to get default configuration from default file <{path}>."
            )
    return config


def _get_global_attribute_config(
    config_metadata: dict,
) -> GlobalAttributesConfiguration | None:
    """Return the configuration of the global attributes."""
    global_attr_metadata = config_metadata.get("global_attributes", None)
    return build_global_attributes_configuration(global_attr_metadata)


def get_configuration(metadata: dict | None = None) -> dict:
    """
    Constructs the configuration from the configuration metadata.

    Given a dictionary containing configuration metadata, the corresponding
    metadata will be used when setting up a dictionary with configuration
    objects. If no metadata is given the default configuration metadata will
    be used.

    Parameters
    ----------
    metadata : dict or None
        A dictionary containing the configuration metadata. If `None` the default
        configuration is used.

    Returns
    -------
    config : dict
        A dictionary containing the configuration.
    """
    config = {}
    if metadata is not None:
        global_attributes_config = _get_global_attribute_config(metadata)
        if global_attributes_config is not None:
            config["global_attributes"] = global_attributes_config
    else:
        config = _get_default_configuration()
    return config


def build_global_attributes_configuration(
    global_attribute_metadata: dict | None = None,
) -> GlobalAttributesConfiguration | None:
    """
    Construct the global attributes configuration object.

    Given a dictionary with the configuration metadata of the global attributes. `None`
    is returned if no configuration is given.

    Parameters
    ----------
    global_attribute_metadata : dict or None
        A dictionary containing the global attributes configuration.

    Returns
    -------
    config_dict : dict
        A dictionary containing the :class:`GlobalAttributesConfiguration`.

    Raises
    ------
    ValueError:
        If the construction of the global attribute configuration object fails.
    """
    global_attributes_configuration = None
    if global_attribute_metadata is not None:
        input_transfer = []
        output_create = []
        try:
            if global_attribute_metadata["input"]["transfer"]:
                for attr_name, attributes in global_attribute_metadata["input"][
                    "transfer"
                ].items():
                    input_transfer.append(
                        InputTransferConfiguration(attr_name, attributes)
                    )
            if global_attribute_metadata["output"]["create"]:
                for attr_name, attribute in global_attribute_metadata["output"][
                    "create"
                ].items():
                    output_create.append(
                        OutputCreateConfiguration(attr_name, attribute)
                    )
            input = GlobalAttributesInputConfiguration(
                global_attribute_metadata["input"]["default"],
                global_attribute_metadata["input"]["drop"],
                input_transfer,
            )
            output = GlobalAttributesOutputConfiguration(
                output_create,
            )
            global_attributes_configuration = GlobalAttributesConfiguration(
                input,
                output,
            )
        except BaseException:
            raise ValueError(
                "Failed to construct global attributes configuration from metadata"
                f"<{global_attribute_metadata}>"
            )
    return global_attributes_configuration


def configure_global_attributes_input(
    cubes: CubeList, config: dict | None = None
) -> None:
    """
    Apply the input configuration of the global attributes to all cubes.

    By default, equalizes all attributes by removing the attributes that are not equal
    between all cubes. A configuration can be used to specify how the global attributes
    should be transferred to the output cube.

    Parameters
    ----------
    cubes : iris.cube.CubeList
        A list of cubes.
    config : dict['GlobalAttributesConfiguration']
        A dictionary containing :class:`GlobalAttributesConfiguration` objects.
    """
    logger.info("Configuring global attributes from input files")
    removed_attributes = set()
    if (config is not None) and ("global_attributes" in config):
        logger.info("Applying global attribute input configuration")
        input_configuration = config["global_attributes"].input
        transfer, attr_not_found = get_transfer_configuration_attributes(
            cubes, input_configuration.transfer
        )
        if attr_not_found:
            logger.debug(
                "Following attributes were not found in all cubes: "
                f"{list(attr_not_found)}"
            )
        replaced_attributes = add_global_attributes(cubes, transfer)
        if replaced_attributes:
            logger.debug(f"Following attributes were replaced: {replaced_attributes}")
        if input_configuration.drop:
            removed_attr = drop_global_attributes(cubes, input_configuration.drop)
            removed_attributes.update(removed_attr)
        if input_configuration.default == "drop":
            removed_attr = default_configuration(cubes, input_configuration)
            removed_attributes.update(removed_attr)
    removed_attr = equalize_global_attributes(cubes)
    removed_attributes.update(removed_attr)
    if removed_attributes:
        logger.debug(
            f"Attributes were removed to equalize cubes: <{list(removed_attributes)}>."
        )


def configure_global_attributes_output(
    cube: CubeList, config: dict | None = None
) -> None:
    """
    Apply the output configuration of the global attributes to all cubes.

    If no configuration object for the output global attributes is given, no changes
    will be made to the cubes. The `extra_attribues` in the
    :class:`GlobalAttributesConfiguration` can be used to store extra attributes that
    are created during runtime.

    Parameters
    ----------
    cubes : iris.cube.CubeList
        A list of cubes.
    config : dict or None, optional
        A dictionary containing :class:`GlobalAttributesConfiguration` objects.
    """
    logger.info("Configuring global attributes for output file")
    if config is not None:
        logger.info("Applying global attribute output configuration")
        cubes = [cube]
        output_configuration = config["global_attributes"].output
        extra_attributes = config["global_attributes"].extra_attributes
        attributes = get_create_configuration_attributes(
            cubes, output_configuration.create, extra_attributes
        )
        replaced_attributes = add_global_attributes(cubes, attributes)
        if replaced_attributes:
            logger.debug(f"Following attributes were replaced: {replaced_attributes}")


def get_transfer_configuration_attributes(
    cubes: CubeList, transfer: list[InputTransferConfiguration]
) -> tuple[dict, list[str]]:
    """
    Create transfer attributes from the `transfer` configuration.

    Collects values from the cubes and returns a dictionary containing all transfer
    attributes and a list containing attributes that could not be found in all cubes.

    Parameters
    ----------
    cubes : iris.cube.CubeList
        A list of cubes.
    transfer : list['InputTransferConfiguration']
        A list containing :class:`InputTransferConfiguration` objects that describes
        the transfer configuration for the  global attributes in the input files.

    Returns
    -------
    attribute_dict : dict
        A dictionary containing all transfer attributes defined by the
        configurations.
    attributes_not_found : list[str]
        A list of string containing global attributes that could not be found in all
        cubes.

    Raises
    ------
    ValueError
        If a `attribute` defined in the configuration could not be found.
    """
    attribute_dict = {}
    attributes_not_found = set()
    for attribute_config in transfer:
        attr_name = attribute_config.attr_name
        if attribute_config.attributes:
            attr_values, attr_not_found = join_global_attribute_values(
                cubes, attribute_config.attributes
            )
        else:
            raise ValueError(f"Attributes could not be found for <{attr_name}>")
        attributes_not_found.update(attr_not_found)
        if attr_values:
            attribute_dict[attr_name] = ", ".join(attr_values)
    return attribute_dict, list(attributes_not_found)


def create_creation_date(
    offset: timedelta = timedelta(0),
) -> str:
    """Create `UTC` creation date following ISO 8601 format.

    Parameters
    ----------
    offset: timedelta
        timedelta object representing the difference between the local time and
        `UTC`. Default is `timedelta(0)` which gives `UTC` time.

    Returns
    -------
    str
        A string representing the ISO 8601 formatted date based on current datetime.
    """
    time = datetime.now(timezone(offset=offset))
    if offset == timedelta(0):
        return time.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    return time.isoformat(timespec="seconds")


def create_tracking_id() -> str:
    """Generate a uuid tracking id.

    A string formatted UUID.
    """
    return str(uuid.uuid4())


def get_create_configuration_attributes(
    cubes: CubeList,
    attributes: list[OutputCreateConfiguration],
    extra_attributes: dict | None = None,
) -> dict:
    """
    Create attributes from the `create` configuration.

    A `extra_attributes` dictonary can be given to include attributes.

    Parameters
    ----------
    cubes : CubeList
        A iris CubeList with one cube containing the result.
    attributes : list['OutputCreateConfiguration']
        A list containing :class:`OutputCreateConfiguration` objects that describes
        the create configuration for the  global attributes in the output files.
    extra_attributes : dict, optional
        A dictionary containing extra attributes to be included in the global
        attributes.

    Returns
    -------
    attribute_dict : dict
        A dictionary of string containing the names and values of the created global
        attributes.

    """
    fill_value = {
        "NOW": create_creation_date(),
        "TRACKING_ID": create_tracking_id(),
        "GORDIAS_VERSION": f"gordias-{__version__}",
        "CF_CONVENTIONS_VERSION": f"{CF_CONVENTIONS_VERSION}",
    }
    fill_value.update(cubes[0].attributes)
    if extra_attributes is not None:
        fill_value.update(extra_attributes)
    attribute_dict = {}
    for attribute_config in attributes:
        attr_name = attribute_config.attr_name
        attr_value = attribute_config.attribute
        if attr_value:
            try:
                attribute_dict[attr_name] = attr_value.format(**fill_value)
            except KeyError:
                raise KeyError(
                    f"Value could not be found for <{attr_name}> <{attr_value}>"
                )
        else:
            raise ValueError(f"Attribute value could not be found for <{attr_name}>")
    return attribute_dict


def equalize_global_attributes(cubes: CubeList) -> list[str]:
    """
    Remove global attributes that are different between all cubes.

    A list is returned containing the set of removed attributes names and values.

    Parameters
    ----------
    cubes : iris.cube.CubeList
        A list of cubes.

    Returns
    -------
    removed_attributes : list[str]
        A list of string containing the names and values of the removed global
        attributes.
    """
    removed_attributes = equalise_attributes(cubes)
    unique_attributes = set()
    for attribute in removed_attributes:
        if isinstance(attribute, dict):
            for attr_name, attr_value in attribute.items():
                unique_attributes.add(f"{attr_name} = {attr_value}")
    return list(unique_attributes)


def default_configuration(
    cubes: CubeList, config: GlobalAttributesInputConfiguration
) -> list[str]:
    """
    Apply the `default` configuration to all cubes.

    The `default` configuration can either drop all attributes that are not present in
    the transfer configuration or equalize the attributes between cubes. A list is
    returned containing the set of removed attributes names and values.

    Parameters
    ----------
    cubes : iris.cube.CubeList
        A list of cubes.
    config : :class:`GlobalAttributesInputConfiguration`
        A :class:`GlobalAttributesInputConfiguration` object containing the input
        configuration for the global attributes.

    Returns
    -------
    removed_attributes : list[str]
        A list of string containing the names and values of the removed global
        attributes.
    """
    removed_attributes = []
    if config.default == "drop":
        removed_attributes = drop_unspecified_global_attributes(cubes, config)
    if config.default == "equalize":
        removed_attributes = equalize_global_attributes(cubes)
    return removed_attributes


def drop_unspecified_global_attributes(
    cubes: CubeList, config: GlobalAttributesInputConfiguration
) -> list[str]:
    """
    Drop all unspecified global attributes for all cubes.

    Tha attributes that are not specified in the transfer configuration is removed. A
    list is returned containing the set of removed attributes names and values.

    Parameters
    ----------
    cubes : iris.cube.CubeList
        A list of cubes.
    config : :class:`GlobalAttributesInputConfiguration`
        A :class:`GlobalAttributesInputConfiguration` object containing the input
        configuration for the global attributes.

    Returns
    -------
    removed_attributes : list[str]
        A list of string containing the names and values of the removed global
        attributes.
    """
    removed_attributes = []
    if config.transfer is not None:
        attributes_to_keep = [attribute.attr_name for attribute in config.transfer]
        all_attributes = set()
        for cube in cubes:
            all_names = [
                attr_name
                for attr_name in cube.attributes
                if attr_name not in attributes_to_keep
            ]
            all_attributes.update(all_names)
        removed_attributes = drop_global_attributes(cubes, list(all_attributes))
    return removed_attributes


def add_global_attributes(cubes: CubeList, attributes: dict) -> list[str]:
    """
    Add global attributes to all cubes.

    Attributes specified in the dictionary `attributes` will be added. A list
    is returned containing the set of replaced attributes with names and values.

    Parameters
    ----------
    cubes : iris.cube.CubeList
        A list of cubes.
    attributes : dict
        A dictionary containing new global attribute names and values.

    Returns
    -------
    replaced_attributes : list[str]
        A list of string containing the names and values of the replaced global
        attributes.
    """
    replaced_attributes = set()
    if attributes:
        for cube in cubes:
            for attr_name, attr_value in attributes.items():
                if (
                    attr_name in cube.attributes
                    and attr_value != cube.attributes[attr_name]
                ):
                    replaced_attributes.add(
                        f"{attr_name} = {cube.attributes[attr_name]}"
                    )
                cube.attributes[attr_name] = attr_value
    return list(replaced_attributes)


def drop_global_attributes(cubes: CubeList, attributes: list[str]) -> list[str]:
    """
    Drop global attributes for all cubes.

    Given a list `attributes` containing the names of the attributes that should be
    dropped. A list is returned containing the set of removed attributes names and
    values.

    Parameters
    ----------
    cubes : iris.cube.CubeList
        A list of cubes.
    attributes : list[str]
        A list of string with global attribute names to drop.

    Returns
    -------
    removed_attributes : list[str]
        A list of string containing the names and values of the removed global
        attributes.
    """
    removed_attributes = set()
    if attributes:
        for cube in cubes:
            for attr_name in attributes:
                if attr_name in cube.attributes:
                    attr_value = cube.attributes.pop(attr_name, None)
                    removed_attributes.add(f"{attr_name} : {attr_value}")
    return list(removed_attributes)


def join_global_attribute_values(
    cubes: CubeList, attr_names: list[str]
) -> tuple[list[str], list[str]]:
    """
    Join attribute values between all cubes.

    Given a list `attr_names` containing the names of the attributes which values should
    be joined between all cubes. Two lists are returned, the first containing joined
    global attributes and the second containing attributes that could not be found in
    all cubes.

    Parameters
    ----------
    cubes : iris.cube.CubeList
        A list of cubes.
    attr_names : list[str]
        A list of string containing global attribute names to join.

    Returns
    -------
    joined_attr_values : list[str]
        A list of string containing joined global attributes.
    attributes_not_found : list[str]
        A list of string containing global attribute names that could not be found in
        all cubes.
    """
    joined_attr_values = set()
    attributes_not_found = set()
    for cube in cubes:
        attr_values = []
        for attr_name in attr_names:
            if attr_name in cube.attributes:
                attr_values.append(cube.attributes[attr_name])
            else:
                attributes_not_found.add(attr_name)
        if attr_values:
            joined_attr_values.add("_".join(attr_values))
    return list(joined_attr_values), list(attributes_not_found)
