from crispy_forms import bootstrap, helper, layout
from django.contrib.auth import mixins as auth_mixins
from django.contrib.sites import shortcuts
from django.views import generic
from rules.contrib import views as rules_views

from . import models


class Gestalt(rules_views.PermissionRequiredMixin, generic.DetailView):
    model = models.Gestalt
    permission_required = 'entities.view_gestalt'


class GestaltSettings(rules_views.PermissionRequiredMixin, generic.TemplateView):
    permission_required = 'entities.change_gestalt'
    template_name = 'entities/gestalt_settings.html'


class GroupDetail(rules_views.PermissionRequiredMixin, generic.DetailView):
    model = models.Group
    permission_required = 'entities.view_group'


class GroupUpdate(rules_views.PermissionRequiredMixin, generic.UpdateView):
    fields = ['address', 'date_founded', 'name', 'slug', 'url']
    model = models.Group
    permission_required = 'entities.change_group'

    def get_form(self):
        DOMAIN = shortcuts.get_current_site(self.request).domain
        form = super().get_form()
        form.helper = helper.FormHelper()
        form.helper.layout = layout.Layout(
                'name',
                layout.Field('address', rows=4),
                'url',
                'date_founded',
                bootstrap.PrependedText('slug', '%(domain)s/' % {'domain': DOMAIN }),
                bootstrap.FormActions(layout.Submit('submit', 'Angaben speichern')),
                )
        return form
