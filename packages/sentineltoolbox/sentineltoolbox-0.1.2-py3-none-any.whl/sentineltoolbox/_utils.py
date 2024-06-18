from pathlib import Path, PurePosixPath

from sentineltoolbox.typedefs import Credentials


def split_protocol(url: str) -> tuple[set[str], PurePosixPath]:
    url_str = str(url)
    if "://" in url_str:
        parts = url_str.split("://")
        protocol = parts[0]
        path = parts[1]
        if not protocol:
            protocol = "file"
    else:
        protocol = "file"
        path = url_str
    return set(protocol.split("::")), PurePosixPath(path)


def fix_url(url: str) -> str:
    """
    Fix url to get always same protocols and protocol order.

    >>> fix_url("test.txt")
    'file://test.txt'
    >>> fix_url("/d/test.txt")
    'file:///d/test.txt'
    >>> fix_url("D:\\test.txt")
    'file://D:\\test.txt'
    >>> fix_url("s3://test")
    's3://test'
    >>> fix_url("s3://")
    's3://'
    >>> fix_url("://test")
    'file://test'
    >>> fix_url("://")
    'file://'
    >>> fix_url("zip::s3://")
    'zip::s3://'
    >>> fix_url("s3::zip://")
    'zip::s3://'
    >>> fix_url("s3://test.zip")
    'zip::s3://test.zip'


    :param url:
    :return:
    """
    protocols, relurl = split_protocol(url)
    is_zip = "zip" in protocols or Path(str(url)).suffix == ".zip"
    if is_zip:
        protocols.add("zip")
    valid_protocols = []
    for p in ["zip", "s3"]:
        if p in protocols:
            valid_protocols.append(p)
            protocols.remove(p)
    protocol = "::".join(valid_protocols + list(protocols))
    if str(relurl) == ".":
        return f"{protocol}://"
    else:
        return f"{protocol}://{relurl}"


def _is_s3_url(url: str) -> bool:
    protocols, path = split_protocol(url)
    return "s3" in protocols


def _credential_required(url: str, credentials: Credentials | None) -> bool:
    protocols, path = split_protocol(url)
    return "s3" in protocols and credentials is None
