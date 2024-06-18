from pathlib import Path, PurePosixPath
from typing import Any

import fsspec

from sentineltoolbox._utils import _credential_required, fix_url, split_protocol
from sentineltoolbox.configuration import Configuration
from sentineltoolbox.models.credentials import S3BucketCredentials
from sentineltoolbox.readers._utils import is_eopf_adf
from sentineltoolbox.typedefs import Credentials, PathOrPattern


def get_fsspec_filesystem(
    path_or_pattern: PathOrPattern,
    credentials: Credentials | None = None,
    **kwargs: Any,
) -> tuple[Any, PurePosixPath]:
    if "filesystem" in kwargs:
        return kwargs["filesystem"]
    else:
        url, credentials = get_url_and_credentials(path_or_pattern, credentials, **kwargs)
        protocols, relurl = split_protocol(url)
        if credentials:
            return fsspec.filesystem(**credentials.to_kwargs(target=fsspec.filesystem)), relurl
        else:
            return fsspec.filesystem("::".join(protocols)), relurl


def get_url_and_credentials(
    path_or_pattern: PathOrPattern,
    credentials: Credentials | None = None,
    **kwargs: Any,
) -> tuple[str, Credentials | None]:

    if isinstance(path_or_pattern, (str, Path)):
        url = fix_url(str(path_or_pattern))
        conf = Configuration.instance()
        secret_alias = conf.get_secret_alias(url)
        if secret_alias:
            kwargs["secret_alias"] = secret_alias
        if _credential_required(url, credentials):
            credentials = S3BucketCredentials.from_env(**kwargs)
    elif is_eopf_adf(path_or_pattern):
        url = str(path_or_pattern.path.original_url)
        if _credential_required(url, credentials):
            storage_options = path_or_pattern.store_params["storage_options"]
            credentials = S3BucketCredentials.from_kwargs(**storage_options)
    else:
        raise NotImplementedError(f"path {path_or_pattern} of type {type(path_or_pattern)} is not supported yet")

    return url, credentials
