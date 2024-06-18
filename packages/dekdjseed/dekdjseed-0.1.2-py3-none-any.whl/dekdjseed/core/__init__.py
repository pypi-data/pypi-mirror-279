import time
from collections import OrderedDict
from django.apps import apps
from django.db import models
from django.contrib.contenttypes.models import ContentType
from .utils.model import sorted_models, turn_off_auto_add, is_model_exists, get_generic_fk_info, get_generic_fk_fields
from .load import SeedLoader
from .fake import Guesser
from .fake.primary import get_int, get_str


class DekDjSeedException(Exception):
    pass


def create_project_entities(seed=None):
    seed = seed or time.time_ns()
    print(f'Current seed: {seed}')
    guesser = Guesser()
    for app_config in apps.get_app_configs():
        create_app_entities(app_config, guesser)


def create_app_entities(app_config, guesser):
    f'{app_config.name}.seed'
    for model in sorted_models(app_config):
        create_model_entities(model, guesser)


def create_model_entities(model_cls, guesser):
    manager = model_cls.objects.db_manager()

    loader = SeedLoader.from_module(f'{model_cls._meta.app_config.name}.seed', guesser)

    if not loader.get_model_config_value(model_cls, 'auto_add', False, model_cls):
        turn_off_auto_add(manager.model)

    generic_fk_info = get_generic_fk_info(model_cls)
    generic_fk_fields = get_generic_fk_fields(model_cls)

    for entity_index in range(loader.get_model_config_value(model_cls, 'number', 1, model_cls)):
        def get_custom_value(fd, dv, *args):
            data = {**faker_data, **faker_data_many_to_many, **custom_data}
            v = loader.get_model_field_value(model_cls, fd.name, data, dv, model_cls, entity_index, *args)
            cancel_map[fd.name] = data.pop('__cancel__', False)
            custom_data.update({k: v for k, v in custom_data.items() if k.startswith('__')})
            return dv if v is loader.EMPTY_VALUE else v

        cancel_map = {}
        faker_data = {}
        faker_data_many_to_many = OrderedDict()
        custom_data = {}

        count_check_unique = 0
        while True:
            faker_data = {}

            for gfk, ct, fk in generic_fk_info:
                field = model_cls._meta.get_field(gfk)
                value = get_custom_value(field, None)
                if value is not None:
                    faker_data[field.name] = value
                    # for is_model_exists
                    faker_data[ct] = ContentType.objects.get_for_model(value.__class__)
                    faker_data[fk] = value.pk

            for field in model_cls._meta.fields:
                if field.name in generic_fk_fields:
                    continue
                if field.primary_key:
                    if field.auto_created:
                        continue
                    if field.max_length is not None:
                        faker_data[field.name] = get_str()[: field.max_length]
                    else:
                        faker_data[field.name] = get_int()
                if field.has_default():
                    faker_data[field.name] = get_custom_value(field, field.get_default())
                    continue
                if isinstance(field, (models.OneToOneField, models.ForeignKey)):
                    array = get_custom_value(field, list(field.related_model.objects.all()))
                    if array:
                        faker_data[field.name] = array if isinstance(array, models.Model) \
                            else guesser.random_sample(array, 1)[0]
                    continue
                formatter = guesser.field_guess_format(field)
                if formatter:
                    faker_data[field.name] = get_custom_value(field, formatter())
                    continue
                # max length restriction check
                if field.max_length is not None:
                    faker_data[field.name] = faker_data[field.name][: field.max_length]

            if not is_model_exists(model_cls, faker_data):
                break
            count_check_unique += 1
            if count_check_unique >= 10000:
                raise DekDjSeedException(f'{model_cls} check unique do not passed, data: {faker_data}')

        for fk in generic_fk_fields:
            faker_data.pop(fk, None)

        if not any(cancel_map.values()):
            obj = manager.create(**faker_data)

            for field in model_cls._meta.many_to_many:
                if field.remote_field.through._meta.auto_created:
                    faker_data_many_to_many[field.name] = get_custom_value(field,
                                                                           list(field.related_model.objects.all()),
                                                                           obj)

            for field_name, related_obj_list in faker_data_many_to_many.items():
                for related_obj in related_obj_list:
                    getattr(obj, field_name).add(related_obj)
