import django.core.urlresolvers
from django import shortcuts
from django.contrib.contenttypes import models as contenttypes
from django.views import generic
from django.views.generic import edit

from . import forms, models
from content import models as content_models
from core.views import base
from features.associations import models as associations
from features.contributions import views as contributions
from features.groups import models as groups


class ContentMixin:
    def get_context_data(self, **kwargs):
        kwargs['content'] = self.get_content()
        return super().get_context_data(**kwargs)

    def get_content(self):
        if 'content_pk' in self.kwargs:
            return content_models.Content.objects.get(
                    pk=self.kwargs['content_pk'])
        return None

    def get_grandparent(self, parent):
        if isinstance(parent, content_models.Content):
            if parent.groups.exists():
                return parent.groups.first()
            else:
                return parent.author
        else:
            return None


class Content(base.PermissionMixin, contributions.ContributionFormMixin, generic.DetailView):
    permission_required = 'content.view'
    permission_required_post = 'content.comment'
    model = associations.Association
    template_name = 'articles/detail.html'

    form_class = forms.Comment

    def get_object(self, queryset=None):
        entity = shortcuts.get_object_or_404(groups.Group, slug=self.kwargs['entity_slug'])
        return shortcuts.get_object_or_404(
                self.model,
                entity_id=entity.id,
                entity_type=contenttypes.ContentType.objects.get_for_model(entity),
                slug=self.kwargs['association_slug'])


class Update(base.PermissionMixin, generic.UpdateView):
    permission_required = 'content.create_version'
    model = associations.Association
    form_class = forms.Update
    template_name = 'content/update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user.gestalt
        return kwargs

    def get_initial(self):
        return {
                'title': self.object.container.title,
                'text': self.object.container.versions.last().text,
                }

    def get_object(self):
        entity = shortcuts.get_object_or_404(groups.Group, slug=self.kwargs['entity_slug'])
        return shortcuts.get_object_or_404(
                associations.Association,
                entity_id=entity.id,
                entity_type=contenttypes.ContentType.objects.get_for_model(entity),
                slug=self.kwargs['association_slug'])
