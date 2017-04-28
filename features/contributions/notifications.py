from django import db
from django.utils import crypto

from core import notifications
from features.conversations import models as conversations
from features.gestalten import models as gestalten
from . import models


class Contributed(notifications.Notification):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contribution = kwargs['contribution']

    def get_message_ids(self):
        my_id = self.contribution.get_unique_id()
        previous_texts = self.contribution.container.contributions.exclude(
                id=self.contribution.id)
        thread_obj = previous_texts.first()
        parent_obj = previous_texts.last()
        parent_id = parent_obj.get_unique_id() if parent_obj else None
        ref_ids = []
        if thread_obj:
            thread_id = thread_obj.get_unique_id()
            if thread_id != parent_id:
                ref_ids.append(thread_id)
        return my_id, parent_id, ref_ids

    def get_recipients(self):
        # find set of recipients
        recipients = set(self.contribution.container.get_authors())
        recipients.update(set(self.contribution.container.get_associated_gestalten()))
        for group in self.contribution.container.get_associated_groups():
            recipients.update(set(gestalten.Gestalt.objects.filter(
                memberships__group=group)))
        # assign a reply key to each recipient
        result = {}
        for gestalt in recipients:
            while True:
                try:
                    key = crypto.get_random_string(
                            length=15, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')
                    models.ReplyKey.objects.create(
                            gestalt=gestalt, key=key, contribution=self.contribution)
                    result[gestalt] = {'reply_key': key}
                    break
                except db.IntegrityError:
                    pass
        return result

    def get_sender(self):
        return self.contribution.author

    def get_subject(self):
        prefix = 'Re: '
        if (self.contribution.container_type == conversations.Conversation.get_content_type()
                and self.contribution.container.contributions.first() == self.contribution):
            prefix = ''
        slugs = self.contribution.container.get_associated_groups().values_list(
                'slug', flat=True)
        groups = '[{}] '.format(','.join(slugs)) if slugs else ''
        return prefix + groups + self.contribution.container.subject

    def get_template_name(self):
        if self.contribution.container.is_conversation:
            name = 'conversations/contributed.txt'
        else:
            name = 'content/contributed.txt'
        return name
