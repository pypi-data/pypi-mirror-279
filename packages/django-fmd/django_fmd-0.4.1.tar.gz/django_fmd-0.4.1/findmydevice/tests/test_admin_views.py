from bx_django_utils.admin_extra_views.utils import reverse_admin_extra_view
from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker

from findmydevice.admin_views import WebPageRedirectView


class AdminViewsTestCase(TestCase):
    def test_web_page_redirect_view(self):
        url = reverse_admin_extra_view(WebPageRedirectView)
        self.assertEqual(url, '/admin/public/find-my-device-location-web-page/')

        user = baker.make(User, is_staff=True)
        self.client.force_login(user)

        response = self.client.get(url, follow=False)
        self.assertRedirects(
            response,
            expected_url='/index.html',
            fetch_redirect_response=False,
        )
