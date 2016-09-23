from . import models
from datetime import date
from django import dispatch
from django.conf import settings
from django.contrib.sites import models as sites_models
from django.core import urlresolvers
from django.db.models import signals


@dispatch.receiver(signals.pre_save, sender=models.Group)
def group_pre_save(sender, instance, **kwargs):
    group = instance
    if not group.address:
        group.address = group.name
    if not group.date_founded:
        group.date_founded = date.today()


@dispatch.receiver(signals.post_save, sender=models.Group)
def group_post_save(sender, instance, created, **kwargs):
    if created and not instance.url:
        instance.url = '{protocol}://{domain}{path}'.format(
                protocol=settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL,
                domain=sites_models.Site.objects.get_current().domain,
                path=urlresolvers.reverse('group', args=[instance.slug]),
                )
        instance.save()
