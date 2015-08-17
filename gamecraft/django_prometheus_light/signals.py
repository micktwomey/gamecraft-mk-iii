import django.db.models.signals
import django.core.signals
from django.dispatch import receiver

import webob

from prometheus_client import Counter

request_finished_counter = Counter('django_signal_request_started_count',
                                   'Django HTTP Request Started Signal',
                                   ['method', 'path'])


@receiver(django.core.signals.request_started, dispatch_uid='prometheus_django_request_started')
def prometheus_django_request_started(sender, **kwargs):
    environ = kwargs['environ']
    request = webob.Request(environ)
    request_finished_counter.labels({
        'method': request.method,
        'path': request.path,
    }).inc()


models_pre_init_counter = Counter('django_signal_models_pre_init_count',
                                  'Django model __init__ about to be called',
                                  ['app_label', 'model_name'])


@receiver(django.db.models.signals.pre_init, dispatch_uid='prometheus_django_models_pre_init')
def prometheus_django_models_pre_init(sender, **kwargs):
    models_pre_init_counter.labels({
        'app_label': sender._meta.app_label,
        'model_name': sender._meta.model_name,
    }).inc()


models_post_init_counter = Counter('django_signal_models_post_init_count',
                                   'Django model __init__ called',
                                   ['app_label', 'model_name'])


@receiver(django.db.models.signals.post_init, dispatch_uid='prometheus_django_models_post_init')
def prometheus_django_models_post_init(sender, **kwargs):
    models_post_init_counter.labels({
        'app_label': sender._meta.app_label,
        'model_name': sender._meta.model_name,
    }).inc()


models_pre_save_counter = Counter('django_signal_models_pre_save_count',
                                  'Django model save() about to be called',
                                  ['app_label', 'model_name', 'raw'])


@receiver(django.db.models.signals.pre_save, dispatch_uid='prometheus_django_models_pre_save')
def prometheus_django_models_pre_save(sender, **kwargs):
    models_pre_save_counter.labels({
        'app_label': sender._meta.app_label,
        'model_name': sender._meta.model_name,
        'raw': kwargs['raw']
    }).inc()


models_post_save_counter = Counter('django_signal_models_post_save_count',
                                   'Django model save() called',
                                   ['app_label', 'model_name', 'raw', 'created'])


@receiver(django.db.models.signals.post_save, dispatch_uid='prometheus_django_models_post_save')
def prometheus_django_models_post_save(sender, **kwargs):
    models_post_save_counter.labels({
        'app_label': sender._meta.app_label,
        'model_name': sender._meta.model_name,
        'raw': kwargs['raw'],
        'created': kwargs['created']
    }).inc()


models_pre_delete_counter = Counter('django_signal_models_pre_delete_count',
                                    'Django model delete() about to be called',
                                    ['app_label', 'model_name'])


@receiver(django.db.models.signals.pre_delete, dispatch_uid='prometheus_django_models_pre_delete')
def prometheus_django_models_pre_delete(sender, **kwargs):
    models_pre_delete_counter.labels({
        'app_label': sender._meta.app_label,
        'model_name': sender._meta.model_name,
    }).inc()


models_post_delete_counter = Counter('django_signal_models_post_delete_count',
                                     'Django model delete() called',
                                     ['app_label', 'model_name'])


@receiver(django.db.models.signals.post_delete, dispatch_uid='prometheus_django_models_post_delete')
def prometheus_django_models_post_delete(sender, **kwargs):
    models_post_delete_counter.labels({
        'app_label': sender._meta.app_label,
        'model_name': sender._meta.model_name,
    }).inc()


models_class_prepared_counter = Counter('django_signal_models_class_prepared_count',
                                        'Django model prepared',
                                        ['app_label', 'model_name'])


@receiver(django.db.models.signals.class_prepared,
          dispatch_uid='prometheus_django_models_class_prepared')
def prometheus_django_models_class_prepared(sender, **kwargs):
    models_class_prepared_counter.labels({
        'app_label': sender._meta.app_label,
        'model_name': sender._meta.model_name,
    }).inc()
