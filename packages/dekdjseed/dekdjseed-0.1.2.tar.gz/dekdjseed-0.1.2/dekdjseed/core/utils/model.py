from toposort import toposort_flatten
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey


def turn_off_auto_add(model_cls):
    for field in model_cls._meta.fields:
        if getattr(field, "auto_now", False):
            field.auto_now = False
        if getattr(field, "auto_now_add", False):
            field.auto_now_add = False


def get_model_dependencies(models):
    dep_dict = {}
    dep_class_map = {}

    for model in models:
        dependencies = set()
        model_replacement = '{}.{}'.format(
            model.__module__,
            model.__name__
        )

        if model_replacement not in dep_class_map:
            dep_class_map[model_replacement] = model

        for field in model._meta.get_fields():
            if ((field.many_to_one is True or field.many_to_many is True or field.one_to_one is True) and
                    field.concrete and field.blank is False):

                related_model = field.related_model
                related_model_type = '{}.{}'.format(
                    related_model.__module__,
                    related_model.__name__
                )
                replacement = related_model_type

                if related_model_type not in dep_class_map:
                    dep_class_map[related_model_type] = related_model

                dependencies.add(replacement)

        dep_dict[model_replacement] = dependencies

    return dep_dict, dep_class_map


def sorted_models(app_config):
    dep_dict, dep_class_map = get_model_dependencies(app_config.get_models())
    return [dep_class_map[x] for x in toposort_flatten(dep_dict)]


def get_model_unique_fields(model_cls):
    result = []
    for field in model_cls._meta.fields:
        if not field.auto_created and field.unique:
            result.append([field])
    result.extend([[model_cls._meta.get_field(name) for name in pairs] for pairs in model_cls._meta.unique_together])
    return result


def is_model_exists(model_cls, data):
    def pkg_filter(k, v):
        if v is None:
            return f'{k}__isnull', True
        return k, v

    fields_list = get_model_unique_fields(model_cls)
    if not fields_list:
        return False
    query = Q()
    for fields in fields_list:
        kv = [pkg_filter(field.name, data.get(field.name)) for field in fields]
        query |= Q(**{item[0]: item[1] for item in kv})
    return model_cls.objects.filter(query).exists()


def get_generic_fk_info(model_cls):
    result = []
    for field in model_cls._meta.private_fields:
        if isinstance(field, GenericForeignKey):
            result.append((field.name, field.ct_field, field.fk_field))
    return result


def get_generic_fk_fields(model_cls):
    result = set()
    for item in get_generic_fk_info(model_cls):
        result.add(item[1])
        result.add(item[2])
    return result
