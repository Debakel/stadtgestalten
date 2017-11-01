import datetime

import django
from django.contrib.contenttypes import fields as contenttypes
from django.contrib.contenttypes.fields import GenericRelation
from django.core import urlresolvers
from django.db import models
from sorl.thumbnail import get_thumbnail

import core.models
from core import colors
from features.gestalten import models as gestalten


def validate_slug(slug):
    if slug in django.conf.settings.ENTITY_SLUG_BLACKLIST:
        raise django.core.exceptions.ValidationError(
                'Die Adresse \'%(slug)s\' ist reserviert und darf nicht verwendet werden.',
                params={'slug': slug}, code='reserved')
    if gestalten.Gestalt.objects.filter(user__username=slug).exists():
        raise django.core.exceptions.ValidationError(
                'Die Adresse \'%(slug)s\' ist bereits vergeben.',
                params={'slug': slug}, code='in-use')


class Group(core.models.Model):
    is_group = True

    date_created = models.DateField(
            auto_now_add=True)
    gestalt_created = models.ForeignKey(
            'gestalten.Gestalt',
            null=True,
            blank=True,
            related_name='+')
    name = models.CharField(
            'Name',
            max_length=255)
    score = models.IntegerField(default=0)
    slug = models.SlugField(
            'Adresse der Gruppenseite', blank=True, null=True, unique=True,
            validators=[validate_slug])

    address = models.TextField(
            'Anschrift',
            blank=True)
    avatar = core.models.ImageField(blank=True)
    avatar_color = models.CharField(
            max_length=7,
            default=colors.get_random_color)
    date_founded = models.DateField(
            'Gruppe gegründet', blank=True, default=datetime.date.today)
    description = models.TextField(
            'Kurzbeschreibung',
            blank=True,
            default='',
            max_length=200)
    logo = core.models.ImageField(blank=True)
    url = models.URLField(
            'Adresse im Web',
            blank=True)
    url_import_feed = models.BooleanField(
            'Beiträge von Website übernehmen', default=False,
            help_text='Öffentliche Beiträge der angegebenen Website automatisch auf '
            'Stadtgestalten veröffentlichen, wenn technisch möglich')

    closed = models.BooleanField(
            'Geschlossene Gruppe',
            default=False,
            help_text='Nur Mitglieder können neue Mitglieder aufnehmen.')

    tags = contenttypes.GenericRelation(
            'tags.Tagged',
            content_type_field='tagged_type',
            object_id_field='tagged_id',
            related_query_name='group')

    associations = django.contrib.contenttypes.fields.GenericRelation(
            'associations.Association', content_type_field='entity_type',
            object_id_field='entity_id', related_query_name='group')

    members = models.ManyToManyField(
            'gestalten.Gestalt', through='memberships.Membership',
            through_fields=('group', 'member'), related_name='groups')

    subscriptions = GenericRelation(
            'subscriptions.Subscription', content_type_field='subscribed_to_type',
            object_id_field='subscribed_to_id', related_query_name='group')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return urlresolvers.reverse(
                'entity', args=[type(self).objects.get(pk=self.pk).slug])

    def get_cover_url(self):
        url = None
        intro_gallery = self.associations.filter_galleries().filter(pinned=True, public=True) \
            .order_content_by_time_created().first()
        if intro_gallery:
            first_image_file = intro_gallery.container.gallery_images.first().image.file
            url = get_thumbnail(first_image_file, '366x120', crop='center').url
        return url

    # FIXME: move to template filter
    # TODO: when removed check api
    def get_initials(self):
        import re
        # we prefer initials for all non-trivial terms - but we collect the other initials, as well
        initials = ''
        initials_without_short_terms = ''
        for w in self.name.split():
            m = re.search('[a-zA-Z0-9]', w)
            if not m:
                continue
            initials += m.group(0)
            if w.lower() not in ("der", "die", "das", "des", "dem",
                                 "den", "an", "am", "um", "im", "in"):
                initials_without_short_terms += m.group(0)
        # prefer the non-trivial one - otherwise pick the full one (and hope it is not empty)
        return initials_without_short_terms if initials_without_short_terms else initials
