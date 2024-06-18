from bx_django_utils.admin_extra_views.base_view import AdminExtraViewMixin
from bx_django_utils.admin_extra_views.datatypes import AdminExtraMeta, PseudoApp
from bx_django_utils.admin_extra_views.registry import register_admin_view
from django.views.generic import RedirectView


public_app = PseudoApp(meta=AdminExtraMeta(name='public'))


@register_admin_view(pseudo_app=public_app)
class WebPageRedirectVire(AdminExtraViewMixin, RedirectView):
    meta = AdminExtraMeta(name='Find My Device - Location Web Page')
    url = '/index.html'
