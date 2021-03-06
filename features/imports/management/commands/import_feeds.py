import datetime
import re
import time

import django
import feedparser
import requests

import core
from features.associations import models as associations
from features.content import models as content
from features.gestalten import models as gestalten
from features.groups import models as groups
from features.imports import models


class Command(django.core.management.base.BaseCommand):

    FEED_RE = (
            r'<link\s+[^>]*'
            r'(?:type=[\"\']application/(?:rss|atom)\+xml[\"\']\s+[^>]*'
            r'href=[\"\']([^\"\']+)[\"\']'
            r'|href=[\"\']([^\"\']+)[\"\']\s+[^>]*'
            r'type=[\"\']application/(?:rss|atom)\+xml[\"\'])'
            r'[^>]*>')

    def handle(self, *args, **options):
        author = gestalten.Gestalt.objects.get(
            id=django.conf.settings.STADTGESTALTEN_FEEDS_IMPORTER_USER_ID)
        for group in groups.Group.objects.filter(url_import_feed=True):
            try:
                r = requests.get(group.url, headers={'User-Agent': 'Stadtgestalten'})
                matches = re.findall(self.FEED_RE, r.text)
                for i, match_groups in enumerate(matches):
                    feed_url = match_groups[0] or match_groups[1]
                    if i > 0:
                        # print('{}: Ignoring feed {}'.format(group, feed_url))
                        continue
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries:
                        key = entry.get('id', entry.get('link'))
                        if key and not models.Imported.objects.filter(key=key).exists():
                            title = entry.get('title')
                            text = entry.get('summary')
                            if title and text:
                                c = content.Content.objects.create(title=title)
                                link = entry.get('link')
                                if link:
                                    text = '{}\n\n{}'.format(text, link)
                                v = content.Version.objects.create(
                                        author=author, content=c, text=text)
                                t = entry.get('published_parsed')
                                if t:
                                    t = datetime.datetime.fromtimestamp(time.mktime(t))
                                    tz = django.utils.timezone.get_current_timezone()
                                    v.time_created = tz.localize(t)
                                    v.save()
                                slug = core.models.get_unique_slug(
                                        associations.Association, {
                                            'entity_id': group.id,
                                            'entity_type': group.content_type,
                                            'slug': core.text.slugify(title),
                                            })
                                associations.Association.objects.create(
                                        entity_type=group.content_type, entity_id=group.id,
                                        container_type=c.content_type, container_id=c.id,
                                        public=True, slug=slug)
                                models.Imported.objects.create(key=key)
            except (requests.exceptions.ChunkedEncodingError,
                    requests.exceptions.ConnectionError):
                pass
