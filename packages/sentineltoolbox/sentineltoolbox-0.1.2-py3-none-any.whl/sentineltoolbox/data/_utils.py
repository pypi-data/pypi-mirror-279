from pathlib import Path
from typing import Any

from sentineltoolbox.models.credentials import S3BucketCredentials
from sentineltoolbox.typedefs import Credentials, PathOrPattern


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


def _credential_required(url: str, credentials: Credentials | None) -> bool:
    return url.startswith("s3://") and credentials is None


def get_url_and_credentials(
    path_or_pattern: PathOrPattern,
    credentials: Credentials | None = None,
    **kwargs: Any,
) -> tuple[str, Credentials | None]:

    if isinstance(path_or_pattern, (str, Path)):
        url = str(path_or_pattern)
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


def fix_kwargs_for_lazy_loading(kwargs: Any) -> None:
    if "chunks" not in kwargs:
        kwargs["chunks"] = {}
    else:
        if kwargs["chunks"] is None:
            raise ValueError(
                "open_datatree(chunks=None) is not allowed. Use load_datatree instead to avoid lazy loading data",
            )
