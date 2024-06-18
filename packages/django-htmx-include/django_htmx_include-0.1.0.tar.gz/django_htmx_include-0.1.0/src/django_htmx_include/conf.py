from __future__ import annotations

from django.conf import settings


class Settings:
    @property
    def HTMX_INCLUDE_CACHE_ALIAS(self) -> str:  # noqa: N802
        return getattr(settings, "HTMX_INCLUDE_CACHE_ALIAS", "default")

    @property
    def HTMX_INCLUDE_CACHE_TIMEOUT(self) -> int | None:  # noqa: N802
        # The number of seconds the value should be stored in the cache.
        # If the setting is not present, Django will use the default timeout
        # argument of the appropriate backend in the CACHES setting.
        return getattr(settings, "HTMX_INCLUDE_CACHE_TIMEOUT", None)

    @property
    def HTMX_SYNC_INCLUDE_REQUEST_ATTR(self) -> str:  # noqa: N802
        return getattr(settings, "HTMX_SYNC_INCLUDE_REQUEST_ATTR", "htmx_sync_include")


conf = Settings()
