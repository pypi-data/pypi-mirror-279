# -*- coding: utf-8 -*-

"""Module for metadata"""
import glob
import logging
import os

import yaml

logger = logging.getLogger(__name__)


def _find_metadata_files_in_dir(directory: str) -> list[str]:
    """Finds all `yml` files in directory"""
    if os.path.isdir(directory):
        return glob.glob(os.path.join(directory, "*.yml"))
    return []


def find_metadata_files(
    metadata_files: str | list[str] | None = None,
) -> list[str]:
    """
    Find metadata files in directories.

    Finds metadata files in default directory `etc`. Additional files can be
    provided through `metadata_files`.

    Parameters
    ----------
    metadata_files: string or list[str]
        A path or a list of paths to external files.

    Returns
    -------
    files: list[str]
        A list containing file paths.
    """
    directories = [os.path.join(os.path.dirname(__file__), "etc")]
    for d in directories:
        logger.info(f"Looking for metadata in directory {d}")
    files = sum(
        [_find_metadata_files_in_dir(directory) for directory in directories], []
    )
    if metadata_files is not None:
        if not isinstance(metadata_files, list):
            metadata_files = [metadata_files]
        for f in metadata_files:
            logger.info(f"Adding metadata from file: {f}")
            files.append(f)
    return files


def load_configuration_metadata(
    metadata_files: str | list[str] | None = None,
) -> dict | None:
    """
    Load configuration metadata.

    A path to a configuration file or a list with paths can be given to the argument
    `metadata_files`. If multiple configurations are given, the last configuration
    found will be used. If no `metadata_files`are given the dafault configuration will
    be used.

    Parameters
    ----------
    metadata_files: string or list[str]
        A path or a list of paths to external configurations.

    Returns
    -------
    config_metadata: dict
        A dictionary containing the configuration metadata.
    """
    config_metadata = None
    for path in find_metadata_files(metadata_files):
        with open(path) as md_file:
            metadata = yaml.safe_load(md_file)
        if "config" in metadata:
            config_metadata = metadata["config"]
            config_path = path
    if config_metadata:
        logger.info(f"Loading configuration with definition from file <{config_path}>.")
    return config_metadata
