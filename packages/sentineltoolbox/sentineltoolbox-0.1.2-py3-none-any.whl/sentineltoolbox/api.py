# all function are loaded in api module instead of in sentineltoolbox/__init__.py
# to avoid to load all dependencies each time.
# For example, pip loads sentineltoolbox to extract __version__ information.
# In this case, we don't want to load all sub packages and associated dependencies

from .converters import convert_to_datatree
from .filesystem_utils import get_fsspec_filesystem
from .flags import create_flag_array, get_flag, update_flag
from .models.credentials import S3BucketCredentials, map_secret_aliases
from .models.filename_generator import (
    AdfFileNameGenerator,
    ProductFileNameGenerator,
    detect_filename_pattern,
)
from .readers._utils import extract_property
from .readers.open_dataset import load_dataset, open_dataset
from .readers.open_datatree import load_datatree, open_datatree
from .readers.open_json import open_json

__all__: list[str] = [
    "S3BucketCredentials",
    "open_dataset",
    "open_datatree",
    "open_json",
    "load_dataset",
    "load_datatree",
    "AdfFileNameGenerator",
    "ProductFileNameGenerator",
    "detect_filename_pattern",
    "map_secret_aliases",
    "create_flag_array",
    "update_flag",
    "get_flag",
    "convert_to_datatree",
    "get_fsspec_filesystem",
    "extract_property",
]
