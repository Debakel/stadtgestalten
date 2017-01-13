from . import models
from crispy_forms import bootstrap, helper, layout
from django import forms
from django.contrib.contenttypes import models as contenttypes
from django.contrib.sites import models as sites
from features.tags import models as tags


class Update(forms.ModelForm):
    tags = forms.CharField(
            label='Schlagworte', required=False,
            help_text='Schlagworte durch Komma getrennt angeben')

    class Meta:
        fields = ('address', 'closed', 'description', 'date_founded', 'name', 'slug', 'url')
        model = models.Group
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['tags'] = ', '.join(self.instance.tags.values_list('name', flat=True))
        self.helper = helper.FormHelper()
        self.helper.layout = layout.Layout(
                'name',
                layout.Field('description', rows=4),
                layout.Field('address', rows=4),
                'url',
                layout.Field('date_founded', data_component='date'),
                'tags',
                bootstrap.PrependedText('slug', '{0}/'.format(
                    sites.Site.objects.get_current().domain)),
                'closed',
                layout.Submit('update', 'Angaben speichern'))

    def save(self, commit=True):
        tag_set = set(self.instance.tags.all())
        for tag in self.cleaned_data['tags'].split(','):
            tag = tag.strip()
            if tag:
                t = tags.Tag.objects.get_or_create(
                        name=tag, tagged_id=self.instance.id,
                        tagged_type=contenttypes.ContentType.objects.get_for_model(
                            self.instance))[0]
                tag_set.discard(t)
        for tag in tag_set:
            tag.delete()
        return super().save(commit)