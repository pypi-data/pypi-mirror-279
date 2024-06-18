import logging
from pathlib import Path
from typing import Any

from sentineltoolbox._utils import split_protocol
from sentineltoolbox.readers._utils import load_toml

logger = logging.getLogger("sentineltoolbox")


class Configuration:
    _current: "Configuration | None" = None

    def __init__(self, **kwargs: Any) -> None:
        self._map_secret_alias_path: dict[str, list[str]] = {}
        self.config_path = Path.home() / ".eopf/sentineltoolbox.toml"
        self._data: dict[Any, Any] = {}
        self.reload()

    def clear(self) -> None:
        self._map_secret_alias_path.clear()

    def reload(self) -> None:
        self.clear()
        if self.config_path.exists():
            self._data.update(load_toml(self.config_path))
        self.map_secret_aliases(self._data.get("secretsmap", {}))

    @classmethod
    def instance(cls, force_new: bool = False) -> "Configuration":
        if cls._current is None or force_new:
            cls._current = Configuration()
        return cls._current

    def map_secret_aliases(self, map: dict[str, str]) -> None:
        if not isinstance(map, dict):
            raise ValueError(f"dict expected, got {map!r}")
        valid_paths: list[str] = []
        for alias, paths in map.items():
            if not isinstance(alias, str):
                logger.warning(f"Invalid alias. expect str, got {alias!r}")
                continue
            if isinstance(paths, str):
                valid_paths = [paths]
            elif isinstance(paths, (list, tuple)):
                # as expected, nothing to do
                valid_paths = paths
            else:
                logger.warning(f"Invalid data for {alias!r}: expect str or list, got {paths!r}")

            current_paths = self._map_secret_alias_path.get(alias, [])
            final_paths = []
            for path in valid_paths:
                if path in current_paths:
                    logger.warning(f"path {path!r} already registered for alias {alias!r}")
                elif isinstance(path, str) and path.startswith("s3://"):
                    final_paths.append(path)
                else:
                    logger.warning(f"Invalid data for {alias!r}: expect str starting with s3://, got {path!r}")

            if final_paths:
                self._map_secret_alias_path.setdefault(alias, []).extend(final_paths)
            else:
                logger.warning(f"Invalid data {valid_paths!r}: alias {alias!r} not updated")

    def get_secret_alias(self, path: str) -> str | None:
        protocols, relurl = split_protocol(path)
        strurl = f"s3://{relurl}"
        for secret_alias, secret_paths in self._map_secret_alias_path.items():
            for secret_path in secret_paths:
                if strurl.startswith(secret_path):
                    return secret_alias
        return None

    @property
    def secret_aliases(self) -> dict[str, list[str]]:
        return {k: v for k, v in self._map_secret_alias_path.items()}
