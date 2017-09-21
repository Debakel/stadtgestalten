import collections

import django

import core
import features
from . import forms, models


class Create(features.content.views.Create):
    template_name = 'polls/create.html'

    form_class = forms.Create


class Detail(features.content.views.DetailBase):
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        # options
        kwargs['options'] = self.object.container.options.order_by('id')

        # votes
        votes = models.Vote.objects.filter(option__poll=self.object.container).order_by(
                'time_updated')
        votes_dict = collections.defaultdict(dict)
        for vote in votes:
            if vote.voter:
                votes_dict[vote.voter][vote.option] = vote
                votes_dict[vote.voter]['latest'] = vote
            else:
                votes_dict[vote.anonymous][vote.option] = vote
                votes_dict[vote.anonymous]['latest'] = vote
        kwargs['votes'] = votes_dict

        # voters
        voters = []
        for vote in votes.order_by('-time_updated'):
            if vote.voter and vote.voter not in voters:
                voters.append(vote.voter)
            elif vote.anonymous and vote.anonymous not in voters:
                voters.append(vote.anonymous)
        kwargs['voters'] = voters[::-1]

        # vote form
        vote_form = getattr(self, 'vote_form', forms.Vote(poll=self.object.container))
        vote_forms = {f.instance.option: f for f in vote_form.votes.forms}
        kwargs['vote_form'] = vote_form
        kwargs['vote_forms'] = vote_forms

        return super().get_context_data(**kwargs)


class Vote(core.views.PermissionMixin, django.views.generic.CreateView):
    permission_required = 'polls.vote'
    model = models.Vote
    form_class = forms.Vote

    def form_invalid(self, form):
        view = Detail(kwargs=self.kwargs, request=self.request)
        view.vote_form = form
        return view.get(self.request)

    def get(self, *args, **kwargs):
        return django.http.HttpResponseRedirect(django.core.urlresolvers.reverse(
            'content', args=[self.kwargs.get('entity_slug'), self.kwargs.get('association_slug')]))

    def get_association(self):
        return django.shortcuts.get_object_or_404(
                features.associations.models.Association,
                django.db.models.Q(group__slug=self.kwargs.get('entity_slug'))
                | django.db.models.Q(gestalt__user__username=self.kwargs.get('entity_slug')),
                slug=self.kwargs.get('association_slug'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated():
            kwargs['instance'] = models.Vote(voter=self.request.user.gestalt)
        kwargs['poll'] = self.association.container
        return kwargs

    def get_permission_object(self):
        self.association = self.get_association()
        return self.association

    def get_success_url(self):
        return self.association.get_absolute_url()
