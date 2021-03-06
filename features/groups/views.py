import django
import django_filters
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse
from django_filters import views as filters_views

import core
from core import fields, views
from core.views import base
from core.views import PermissionMixin
from features.associations import models as associations
from features.associations.filters import ContentFilterSet
from features.groups import models as groups
from . import filters, forms, models


class Mixin:
    '''
    Obsolete: Do not use in new code!
    '''
    def get_context_data(self, **kwargs):
        kwargs['group'] = self.get_group()
        return super().get_context_data(**kwargs)

    def get_group(self):
        for attr in ('object', 'related_object'):
            if hasattr(self, attr):
                instance = getattr(self, attr)
                if isinstance(instance, models.Group):
                    return instance
                if hasattr(instance, 'group'):
                    return instance.group
                if hasattr(instance, 'groups'):
                    return instance.groups.first()
        try:
            if 'group_pk' in self.kwargs:
                return models.Group.objects.get(
                        pk=self.kwargs['group_pk'])
            if 'group_slug' in self.kwargs:
                return models.Group.objects.get(
                        slug=self.kwargs['group_slug'])
            if 'group' in self.request.GET:
                return models.Group.objects.get(
                        slug=self.request.GET['group'])
        except models.Group.DoesNotExist:
            pass
        return None


class Create(views.Create):
    permission_required = 'groups.create_group'

    action = 'Gruppe anlegen'
    menu = 'group'
    # parent = 'group-index'
    title = 'Neue Gruppe'

    model = models.Group

    data_field_classes = (
            fields.current_gestalt('gestalt_created', null=True),
            fields.model_field('name'))


class Detail(
        core.views.PermissionMixin, django_filters.views.FilterMixin,
        django.views.generic.list.MultipleObjectMixin, django.views.generic.DetailView):
    permission_required = 'groups.view'
    model = models.Group
    filterset_class = ContentFilterSet
    paginate_by = 10
    template_name = 'groups/detail.html'

    def get_queryset(self):
        return self.object.associations.ordered_user_content(self.request.user)

    def get_context_data(self, **kwargs):
        associations = self.get_queryset()
        filterset = self.get_filterset(self.get_filterset_class())
        intro_associations = associations.filter(pinned=True).order_by('time_created')
        intro_gallery = intro_associations.filter_galleries().filter(public=True).first()
        if intro_gallery:
            intro_associations = intro_associations.exclude(pk=intro_gallery.pk)
        kwargs['feed_url'] = self.request.build_absolute_uri(
                reverse('group-feed', args=(self.object.pk,)))
        return super().get_context_data(
                associations=associations,
                filter=filterset,
                intro_associations=intro_associations,
                intro_gallery=intro_gallery,
                group=self.object,
                object_list=filterset.qs,
                **kwargs)

    def get_object(self):
        return self.object


class List(base.PermissionMixin, filters_views.FilterView):
    permission_required = 'groups.view_list'
    filterset_class = filters.Group
    paginate_by = 10

    def get_content(self):
        return associations.Association.objects.filter_group_containers().can_view(
                self.request.user)

    def get_queryset(self):
        return groups.Group.objects.order_by('-score')


class Update(PermissionMixin, UpdateView):
    permission_required = 'groups.change'
    model = models.Group
    form_class = forms.Update
    template_name = 'groups/update.html'

    def get_object(self):
        return get_object_or_404(models.Group, slug=self.request.GET.get('group'))


class ImageUpdate(PermissionMixin, UpdateView):
    permission_required = 'groups.change'
    model = models.Group
    fields = ('avatar', 'logo')
    template_name = 'groups/update_images.html'

    def get_object(self):
        return get_object_or_404(models.Group, slug=self.request.GET.get('group'))


class SubscriptionsMemberships(PermissionMixin, TemplateView):
    permission_required = 'groups.change_subscriptions_memberships'
    template_name = 'groups/subscriptions_memberships.html'

    def get_context_data(self, **kwargs):
        kwargs['group'] = self.group
        return super().get_context_data(**kwargs)

    def get_object(self):
        return get_object_or_404(models.Group, slug=self.request.GET.get('group'))

    def get_permission_object(self):
        self.group = super().get_permission_object()
        return self.group
