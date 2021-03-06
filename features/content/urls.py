from . import views
from django.conf import urls

urlpatterns = [
    urls.url(
        r'^(?P<entity_slug>[\w-]+)/(?P<association_slug>[\w-]+)/$',
        views.Detail.as_view(),
        name='content'),

    urls.url(
        r'^stadt/content/(?P<association_pk>[0-9]+)/$',
        views.Permalink.as_view(),
        name='content-permalink'),

    urls.url(
        r'^(?P<entity_slug>[\w-]+)/(?P<association_slug>[\w-]+)/edit/$',
        views.Update.as_view(),
        name='update-content'),
]
