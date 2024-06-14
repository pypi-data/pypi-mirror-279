from django.apps import AppConfig
try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _

class LoducodeUtilsConfig(AppConfig):
    name = 'loducode_utils'
    verbose_name = _('utils')