"""
No public API here.
Use root package to import public function and classes
"""

__all__: list[str] = []

from pathlib import Path
from typing import Any, Union

import datatree
import xarray as xr
import zarr
import zarr.errors
from datatree import DataTree

from sentineltoolbox.converters import convert_to_datatree
from sentineltoolbox.data._utils import (
    _cleaned_kwargs,
    fix_kwargs_for_lazy_loading,
    get_url_and_credentials,
    is_eopf_adf_loaded,
)
from sentineltoolbox.data.json_data import is_json, open_json
from sentineltoolbox.typedefs import Credentials, PathMatchingCriteria, PathOrPattern


def open_eop_datatree(
    filename_or_obj: Union[str, Path],
    **kwargs: Any,
) -> datatree.DataTree[Any]:
    """Open and decode a EOPF-like Zarr product

    Parameters
    ----------
    filename_or_obj: str, Path
        Path to directory in file system or name of zip file.
        It supports passing URLs directly to fsspec and having it create the "mapping" instance automatically.
        This means, that for all of the backend storage implementations supported by fsspec, you can skip importing and
        configuring the storage explicitly.

    kwargs: dict

    Returns
    -------
        datatree.DataTree
    """

    if "chunks" not in kwargs:
        kwargs["chunks"] = {}

    if "backend_kwargs" in kwargs:
        storage_options = kwargs["backend_kwargs"]
        zds = zarr.open_group(filename_or_obj, mode="r", **storage_options)
    else:
        zds = zarr.open_group(filename_or_obj, mode="r")
    ds = xr.open_dataset(filename_or_obj, **kwargs)
    tree_root = datatree.DataTree.from_dict({"/": ds})
    for path in datatree.io._iter_zarr_groups(zds):
        try:
            subgroup_ds = xr.open_dataset(filename_or_obj, group=path, **kwargs)
        except zarr.errors.PathNotFoundError:
            subgroup_ds = xr.Dataset()

        # TODO refactor to use __setitem__ once creation of new nodes by assigning Dataset works again
        node_name = datatree.treenode.NodePath(path).name
        new_node: datatree.DataTree[Any] = datatree.DataTree(name=node_name, data=subgroup_ds)
        tree_root._set_item(
            path,
            new_node,
            allow_overwrite=False,
            new_nodes_along_path=True,
        )
    return tree_root


def open_datatree(
    path_or_pattern: PathOrPattern,
    *,
    credentials: Credentials | None = None,
    match_criteria: PathMatchingCriteria = "last_creation_date",
    **kwargs: Any,
) -> DataTree[Any]:
    """
    Function to open tree data (zarr sentinel product) from bucket or local path and open it as :obj:`datatree.DataTree`

    .. note::

        Data are lazy loaded. To fully load data in memory, prefer :obj:`~sentineltoolbox.api.load_datatree`


    Optional arguments credentials, match_criteria, ... must be specified by key.

    Parameters
    ----------
    Parameters common to all open_* and load_*:
        see :obj:`sentineltoolbox.typedefs` for details on
            - path_or_pattern
            - credentials
            - match_criteria
    """
    if is_eopf_adf_loaded(path_or_pattern) and isinstance(path_or_pattern.data_ptr, datatree.DataTree):
        return path_or_pattern.data_ptr
    url, credentials = get_url_and_credentials(path_or_pattern, credentials=credentials, **kwargs)

    fix_kwargs_for_lazy_loading(kwargs)

    if is_json(url):
        return convert_to_datatree(open_json(url, credentials=credentials, **kwargs))
    else:
        if credentials is not None:
            kwargs["backend_kwargs"] = credentials.to_kwargs(url=url, target="zarr.open_consolidated")
            kwargs["filename_or_obj"] = kwargs["backend_kwargs"].pop("store")
        else:
            kwargs["filename_or_obj"] = url

        kwargs["engine"] = "zarr"

        return open_eop_datatree(**_cleaned_kwargs(kwargs))


def load_datatree(
    path_or_pattern: PathOrPattern,
    *,
    credentials: Credentials | None = None,
    match_criteria: PathMatchingCriteria = "last_creation_date",
    fake_data: str | None = None,
    **kwargs: Any,
) -> DataTree[Any]:
    """
    Function to load tree data (zarr sentinel product) from bucket or local path and load it as :obj:`datatree.DataTree`

    .. warning::
        all data are loaded in memory. Use it only for small data.

        To lazy load data, prefer :obj:`~sentineltoolbox.api.open_datatree`

    Optional arguments credentials, match_criteria, ... must be specified by key.

    Parameters
    ----------
    Parameters common to all open_* and load_*:
        see :obj:`sentineltoolbox.typedefs` for details on
            - path_or_pattern
            - credentials
            - match_criteria
    fake_data, optional
        if set, replace data with fake data. Type of fake data correspond to fake_data mode.
        Use this if you want to manipulate only metadata and attrs
    """
    raise NotImplementedError
