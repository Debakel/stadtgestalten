import django
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.urls import reverse
from haystack.inputs import AutoQuery
from haystack.query import EmptySearchQuerySet, SearchQuerySet

import core
from core.views import PermissionMixin
from features import gestalten, groups
from features.content import views as content
from features.groups.models import Group


class Entity(core.views.PermissionMixin, django.views.generic.View):
    def get(self, request, *args, **kwargs):
        context = self.view.get_context_data(object=self.view.object)
        return self.view.render_to_response(context)

    def get_object(self):
        slug = self.kwargs.get('entity_slug')
        try:
            return Group.objects.get(slug=slug)
        except Group.DoesNotExist:
            return get_object_or_404(gestalten.models.Gestalt, user__username=slug)

    def get_view(self):
        # choose view based on entity type
        entity = self.get_object()
        if entity.is_group:
            view = groups.views.Detail()
        else:
            view = gestalten.views.Detail()

        # set view attributes
        view.object = entity
        view.object_list = None
        view.kwargs = self.kwargs
        view.request = self.request

        return view

    def has_permission(self):
        self.view = self.get_view()
        return self.view.has_permission()


class Index(content.List):
    template_name = 'stadt/index.html'

    def get_context_data(self, **kwargs):
        kwargs['intro_text'] = settings.STADTGESTALTEN_INTRO_TEXT
        kwargs['feed_url'] = self.request.build_absolute_uri(reverse('feed'))
        kwargs['town_name'] = get_current_site(self.request).name.split()[-1]
        return super().get_context_data(**kwargs)


class Privacy(core.views.PageMixin, django.views.generic.TemplateView):
    permission_required = 'stadt.view_privacy'
    template_name = 'entities/privacy.html'
    title = 'Datenschutz'

    def get_context_data(self, **kwargs):
        kwargs['HAS_PIWIK'] = settings.HAS_PIWIK
        return super().get_context_data(**kwargs)


class Search(PermissionMixin, ListView):
    permission_required = 'stadt.search'
    paginate_by = 10
    template_name = 'stadt/search.html'

    def get_queryset(self):
        query_string = self.request.GET.get('q', '').strip()
        if query_string:
            return SearchQuerySet().filter(content=AutoQuery(query_string))
        else:
            return EmptySearchQuerySet()
