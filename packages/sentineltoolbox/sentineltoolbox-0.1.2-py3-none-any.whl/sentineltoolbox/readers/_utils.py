import logging
from pathlib import Path
from typing import Any, BinaryIO, Literal

import tomli
from datatree import DataTree
from xarray import Dataset

logger = logging.getLogger("sentineltoolbox")


L_SUPPORTED_FORMATS = Literal[".json", ".toml", ".txt", None]


def load_toml_fp(fp: BinaryIO) -> dict[str, Any]:
    with fp:
        return tomli.load(fp)


def load_toml(path: Path) -> dict[str, Any]:
    with open(path, mode="rb") as fp:
        return load_toml_fp(fp)


def is_eopf_adf(path_or_pattern: Any) -> bool:
    """

    :param path_or_pattern:
    :return:
    """
    adf = path_or_pattern
    # do not check full module and class name case because it doesn't match convention, it is not logical
    # so ... it may change soon (eopf.computing.abstract.ADF)
    match = adf.__class__.__module__.startswith("eopf") and adf.__class__.__name__.lower() == "adf"
    match = match and hasattr(adf, "name")
    match = match and hasattr(adf, "path")
    match = match and hasattr(adf, "store_params")
    match = match and hasattr(adf, "data_ptr")
    return match


def is_eopf_adf_loaded(path_or_pattern: Any) -> bool:
    """

    :param path_or_pattern:
    :return:
    """
    return is_eopf_adf(path_or_pattern) and path_or_pattern.data_ptr


def _cleaned_kwargs(kwargs: Any) -> dict[str, Any]:
    cleaned = {}
    for kwarg in kwargs:
        if kwarg not in ("secret_alias",):
            cleaned[kwarg] = kwargs[kwarg]
    return cleaned


def fix_kwargs_for_lazy_loading(kwargs: Any) -> None:
    if "chunks" not in kwargs:
        kwargs["chunks"] = {}
    else:
        if kwargs["chunks"] is None:
            raise ValueError(
                "open_datatree(chunks=None) is not allowed. Use load_datatree instead to avoid lazy loading data",
            )


def string_to_slice(s: str) -> slice:
    """
    Convert a string in the format "start:stop:step" to a Python slice object.

    :param s: String representing the slice.
    :return: Corresponding Python slice object.
    """
    # Split the string by colon to get start, stop, and step parts
    parts: list[str | Any] = s.split(":")

    # If the string contains fewer than three parts, append None for missing values
    while len(parts) < 3:
        parts.append(None)

    # Convert the parts to integers or None
    start = int(parts[0]) if parts[0] else None
    stop = int(parts[1]) if parts[1] else None
    step = int(parts[2]) if parts[2] else None

    # Create and return the slice object
    return slice(start, stop, step)


valid_aliases = {"eo:bands": "bands"}
legacy_aliases = {v: k for k, v in valid_aliases.items()}


def valid_alias(part: str) -> str:

    if part in valid_aliases:
        return valid_aliases[part]
    else:
        return part


def legacy_alias(part: str) -> str:
    if part in legacy_aliases:
        return legacy_aliases[part]
    else:
        return part


def fix_property(path: str, value: Any) -> Any:
    if path == "platform" and isinstance(value, str):
        new_value = value.lower()
    else:
        new_value = value
    if value != new_value:
        logger.info(f"{path}: value {value!r} has been fixed to {new_value!r}")
    return new_value


def extract_property(data: DataTree[Any] | Dataset | dict[str, Any], path: str | None = None) -> Any:
    if isinstance(data, (DataTree, Dataset)):
        attrs = data.attrs
    else:
        attrs = data
    stac_discovery = attrs.get("stac_discovery", {})
    properties = stac_discovery.get("properties", attrs.get("properties", attrs))
    if path is None:
        return properties
    else:
        path = path.strip().rstrip("/")
        group = properties
        parts: list[str] = path.split("/")
        for part in parts:
            try:
                valid_part: int | slice | str = int(part)
            except ValueError:
                try:
                    valid_part = string_to_slice(part)
                except ValueError:
                    valid_part = part

            if isinstance(valid_part, (int, slice)):
                group = group[valid_part]
            else:
                valid_name = valid_alias(valid_part)
                legacy_name = legacy_alias(valid_part)
                if valid_name != valid_part:
                    logger.warning(f"{valid_part!r} is deprecated, use {valid_alias(valid_part)!r} instead")
                if valid_name in group:
                    group = group[valid_name]
                elif valid_part in group:
                    group = group[valid_part]
                elif legacy_name in group:
                    group = group[legacy_name]
                else:
                    group = group[valid_part]
        return fix_property(path, group)
