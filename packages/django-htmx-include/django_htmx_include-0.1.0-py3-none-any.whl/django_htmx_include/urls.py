from __future__ import annotations

from django.urls import path

from django_htmx_include.views import HtmxIncludeView

app_name = "htmx_include"

urlpatterns = [
    path("", HtmxIncludeView.as_view(), name="include"),
]
