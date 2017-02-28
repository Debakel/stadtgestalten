import datetime
from email import utils as email_utils
import uuid

from django.apps import apps
from django.conf import settings
from django.contrib.sites import models as sites_models
from django.core import mail
from django.template import loader


class Notification:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @staticmethod
    def format_recipient(gestalt):
        return '{} <{}>'.format(gestalt, gestalt.user.email)

    def get_formatted_recipients(self):
        recipients = self.get_recipients()
        if type(recipients) == dict:
            return [(self.format_recipient(r), with_name)
                    for r, with_name in recipients.items()]
        else:
            return [(self.format_recipient(r), True) for r in recipients]

    def get_sender(self):
        return None

    def get_sender_email(self):
        return settings.DEFAULT_FROM_EMAIL

    def get_subject(self):
        return self.subject

    def get_template_name(self):
        app_label = apps.get_containing_app_config(type(self).__module__).label
        return '{}/{}.txt'.format(
                app_label, type(self).__name__.lower())

    def get_message_ids(self):
        """ generate a unique message ID for this specific email message and related IDs

        Most notification subclasses should implement their own specific message ID generator.
        Some notifications lack unique features, since they can be issued multiple times (e.g.
        group recommendations or membership associations).
        In these cases we pick a random ID. These subclasses do not need to overwrite this method.

        The result is a tuple of three items:
            * unique message ID
            * parent message ID (if available)
            * thread ID and other related messages (if available)
        """
        now_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        uuid_string = uuid.uuid4().hex[:16]
        my_id = '{}.{}'.format(now_string, uuid_string)
        return my_id, None, []

    def send(self):
        for recipient, with_name in self.get_formatted_recipients():
            subject = self.get_subject()
            site = sites_models.Site.objects.get_current()
            context = self.kwargs.copy()
            context.update({'site': site})
            template = loader.get_template(self.get_template_name())
            template.backend.engine.autoescape = False
            body = template.render(context)
            sender = self.get_sender()
            name = '{} via '.format(sender) if sender and with_name else ''
            from_email = '{name}{site} <{email}>'.format(
                    name=name,
                    site=site.name,
                    email=self.get_sender_email())
            headers = {}
            headers['Date'] = email_utils.formatdate(localtime=True)
            message_id, parent_id, reference_ids = self.get_message_ids()
            headers['Message-ID'] = '<{}@{}>'.format(message_id, site.domain)
            if parent_id:
                headers['In-Reply-To'] = '<{}@{}>'.format(parent_id, site.domain)
                if parent_id not in reference_ids:
                    reference_ids.append(parent_id)
            if reference_ids:
                headers['References'] = ' '.join(['<{}@{}>'.format(ref_id, site.domain)
                                                  for ref_id in reference_ids])
            message = mail.EmailMessage(
                    body=body, from_email=from_email, subject=subject,
                    to=[recipient], headers=headers)
            message.send()
