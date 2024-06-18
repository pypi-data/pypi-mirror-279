from __future__ import annotations

from django.test import SimpleTestCase
from django.test.utils import override_settings
from django_htmx_include.conf import conf


class ConfTests(SimpleTestCase):
    def test_sync_include_request_attr_default(self):
        self.assertEqual(conf.HTMX_SYNC_INCLUDE_REQUEST_ATTR, "htmx_sync_include")

    @override_settings(HTMX_SYNC_INCLUDE_REQUEST_ATTR="foo")
    def test_sync_include_request_attr_override(self):
        self.assertEqual(conf.HTMX_SYNC_INCLUDE_REQUEST_ATTR, "foo")

    def test_cache_alias_default(self):
        self.assertEqual(conf.HTMX_INCLUDE_CACHE_ALIAS, "default")

    @override_settings(HTMX_INCLUDE_CACHE_ALIAS="custom")
    def test_cache_alias_override(self):
        self.assertEqual(conf.HTMX_INCLUDE_CACHE_ALIAS, "custom")

    def test_cache_timeout_default(self):
        self.assertEqual(conf.HTMX_INCLUDE_CACHE_TIMEOUT, None)

    @override_settings(HTMX_INCLUDE_CACHE_TIMEOUT=100)
    def test_cache_timeout_override(self):
        self.assertEqual(conf.HTMX_INCLUDE_CACHE_TIMEOUT, 100)
