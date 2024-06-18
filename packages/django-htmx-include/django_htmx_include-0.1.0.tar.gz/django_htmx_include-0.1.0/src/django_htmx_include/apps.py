from __future__ import annotations

from django.apps import AppConfig


class HtmxIncludeAppConfig(AppConfig):
    name = "django_htmx_include"
    verbose_name = "django-htmx-include"

    def ready(self) -> None:
        from django_htmx_include import checks  # noqa: F401
