from unittest import TestCase

import eduid_IdP_html

__author__ = 'ft'


class TestLoad_settings(TestCase):

    def test_load_settings(self):
        settings = eduid_IdP_html.load_settings()
        self.assertTrue(settings['gettext_domain'] is not None)
