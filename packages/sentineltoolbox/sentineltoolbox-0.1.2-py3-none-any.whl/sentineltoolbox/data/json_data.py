import json
from pathlib import Path
from typing import Any

import fsspec
from datatree import DataTree

from sentineltoolbox.data._utils import get_url_and_credentials, is_eopf_adf_loaded
from sentineltoolbox.typedefs import Credentials, PathMatchingCriteria, PathOrPattern


def is_json(path: str) -> bool:
    suffixes: str = "".join(Path(path).suffixes)
    # TODO: path.is_file() and
    return suffixes in {".json", ".json.zip"}


def open_json(
    path_or_pattern: PathOrPattern,
    *,
    credentials: Credentials | None = None,
    match_criteria: PathMatchingCriteria = "last_creation_date",
    **kwargs: Any,
) -> DataTree[Any]:

    if is_eopf_adf_loaded(path_or_pattern) and isinstance(path_or_pattern.data_ptr, dict):
        return path_or_pattern.data_ptr
    url, credentials = get_url_and_credentials(path_or_pattern, credentials=credentials, **kwargs)

    if credentials:
        fs = fsspec.filesystem(**credentials.to_kwargs(target=fsspec.filesystem))
        open_func = fs.open
    else:
        open_func = open

    with open_func(url, "r") as json_fp:
        return json.load(json_fp)
