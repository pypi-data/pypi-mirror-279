from __future__ import annotations

from django.urls import include, path

from tests import views

urlpatterns = [
    path("__htmx-include__/", include("django_htmx_include.urls")),
    path("core/", views.CoreView.as_view(), name="core"),
    path("for_loop/", views.ForLoopView.as_view(), name="for_loop"),
]
