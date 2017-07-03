import django

from django.contrib.admin import site
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from ordered_model.models import OrderedModel


class AppGroupQuerySet(models.QuerySet):
    def as_list(self, request, include_remaining=True):
        # Convert to convienent dict
        model_dicts = {}

        if django.VERSION[0] == 1 and django.VERSION[1] <= 8:
            from .compat.django18 import get_app_list
            original_app_list = get_app_list(site, request)
        else:
            original_app_list = site.get_app_list(request)

        for app in original_app_list:
            for model in app['models']:
                key = '{}.{}'.format(app['app_label'], model['object_name'].lower())
                model_dict = model.copy()
                model_dict.update({
                    'app_label': app['app_label'],
                    'app_url': app['app_url'],
                    'has_module_perms': app['has_module_perms'],
                })
                model_dicts[key] = model_dict

        added = []

        # Create new list based on our groups, using the model_dicts constructed above.
        result = []
        app_list = self.prefetch_related('models', 'applink_set')
        for app in app_list:
            models = []
            for model in app.models.all():
                key = '{}.{}'.format(model.app_label, model.model)
                o = model_dicts.get(key)
                if o:
                    models.append(o)
                    added.append(key)

            for app_link in app.applink_set.all():
                models.append({
                    'name': app_link.name,
                    'app_label': app.slug,
                    'admin_url': app_link.link,
                })

            if models:
                result.append({
                    'name': app.name,
                    'app_label': app.slug,
                    'models': sorted(models, key=lambda m: m['name'])
                })

        if include_remaining:
            other = set(model_dicts.keys()).difference(set(added))
            if other:
                result.append({
                    'name': _('Miscellaneous'),
                    'app_label': 'misc',
                    'models': sorted(
                        [model_dict for key, model_dict in model_dicts.items() if key in other],
                        key=lambda m: m['name'],
                    )
                })

        return result


@python_2_unicode_compatible
class ContentTypeProxy(ContentType):
    class Meta:
        proxy = True
        ordering = ('app_label', 'model')

    def __str__(self):
        return '{}.{}'.format(self.app_label, capfirst(super(ContentTypeProxy, self).__str__()))


@python_2_unicode_compatible
class AppGroup(OrderedModel):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    models = models.ManyToManyField(ContentTypeProxy, blank=True)

    objects = AppGroupQuerySet.as_manager()

    class Meta(OrderedModel.Meta):
        verbose_name = _('application group')
        verbose_name_plural = _('application groups')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AppLink(OrderedModel):
    app_group = models.ForeignKey(AppGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

    class Meta(OrderedModel.Meta):
        verbose_name = _('application link')
        verbose_name_plural = _('application links')

    def __str__(self):
        return self.name