from bx_django_utils.test_utils.html_assertion import (
    HtmlAssertionMixin,
    assert_html_response_snapshot,
)
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse
from django.test import TestCase, override_settings
from model_bakery import baker

import findmydevice
from findmydevice.views.version import VersionView
from findmydevice.views.web_page import FmdWebPageView


@override_settings(SECURE_SSL_REDIRECT=False)
class FmdWebPageTests(HtmlAssertionMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.normal_user = baker.make(User, is_staff=False, is_active=True, is_superuser=False)

    def test_anonymous(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, template_name='fmd/login_info.html')
        self.assertEqual(response.resolver_match.func.view_class, FmdWebPageView)
        self.assert_html_parts(
            response,
            parts=(
                '<title>Log in | Find My Device</title>',
                '<p class="errornote">To find your device, you must be logged in.</p>',
                '<a href="/admin/login/">Log in</a>',
            ),
        )
        assert_html_response_snapshot(response, query_selector=None, validate=False)

    def test_normal_user(self):
        self.client.force_login(self.normal_user)
        response = self.client.get('/')
        assert isinstance(response, FileResponse)
        response2 = HttpResponse(response.getvalue())
        self.assert_html_parts(
            response2,
            parts=(
                '<title>Django Find My Device</title>',
                '<h2>Django Find My Device</h2>',
                '<link rel="stylesheet" href="./static/fmd_externals/style.css">',
                '<script src="./static/fmd_externals/logic.js"></script>',
                '<link rel="icon" href="./static/fmd_externals/favicon.ico">',
            ),
        )
        assert_html_response_snapshot(response2, query_selector=None, validate=False)

    def test_version(self):
        response = self.client.get('/version')
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.resolver_match.func.view_class, VersionView)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('ASCII'), f'v{findmydevice.__version__}')
