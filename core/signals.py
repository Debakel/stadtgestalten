from django import dispatch
from django.db.models import signals
from django.utils import module_loading


def always(instance):
    return True


def connect(
        signal, notification_class, instance=None, predicate=None, senders=[]):
    def receiver(sender, **kwargs):
        if predicate:
            if predicate(kwargs['instance']):
                notification_class(**{instance: kwargs['instance']}).send()
    for sender in senders:
        signal.connect(receiver, sender=sender, weak=False)


def include(module_name):
    module_loading.import_string(module_name + '.connections')


model_created = dispatch.Signal()


def model_saved(sender, **kwargs):
    if kwargs['created']:
        model_created.send(sender, instance=kwargs['instance'])

signals.post_save.connect(model_saved)