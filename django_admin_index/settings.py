from django.conf import settings as django_settings

SHOW_REMAINING_APPS = getattr(django_settings, 'ADMIN_INDEX_SHOW_REMAINING_APPS', False)

SHOW_REMAINING_APPS_TO_SUPERUSERS = getattr(django_settings, 'ADMIN_INDEX_SHOW_REMAINING_APPS_TO_SUPERUSERS', True)