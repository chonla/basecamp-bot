import os
import yaml
from pathlib import Path


class Session:
    def __init__(self, session_key: str):
        self._session_key = session_key
        self._data = {}
        self._ensure_cache_dir()
        self._cache_file = f".botcache/{self._session_key}"
        self._load_cache_if_available()

    def set_value(self, key: str, value: any):
        self._data[key] = value
        self._store()

    def get_value(self, key: str, default_value: any) -> any:
        if key in self._data:
            return self._data[key]
        return default_value

    def _ensure_cache_dir(self):
        os.makedirs('.botcache', exist_ok=True)

    def _load_cache_if_available(self):
        path = Path(self._cache_file)
        if path.is_file():
            with open(self._cache_file, "r") as f:
                self._data = yaml.safe_load(f)

    def _store(self):
        with open(self._cache_file, "w") as f:
            yaml.safe_dump(self._data, f)
