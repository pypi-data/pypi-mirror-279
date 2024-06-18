import random
from django.core.validators import validate_comma_separated_integer_list
from django.utils import timezone
from django.db import models
from django.conf import settings
from faker.factory import Factory
from django.contrib.postgres.fields import ArrayField
from .providers import Provider


def _timezone_format(value):
    if getattr(settings, 'USE_TZ', False):
        return timezone.make_aware(value, timezone.get_current_timezone(), is_dst=False)
    return value


class Guesser:
    def __init__(self, seed=0):
        fake = Factory.create()
        fake.seed(seed)
        self.fake = fake
        self.provider = Provider(fake)

    @property
    def random(self):
        return random

    def random_sample(self, lst, length=1):
        if not lst:
            return []
        lst = list(lst)
        result = random.sample(lst, min(len(lst), length))
        if isinstance(lst, str):
            return ''.join(result)
        elif isinstance(lst, bytes):
            return b''.join(result)
        return result

    def field_guess_format(self, field):
        provider = self.provider

        if field.choices:
            return lambda : random.choice(field.choices)[0]

        if isinstance(field, models.DurationField): return lambda : provider.duration()
        if isinstance(field, models.UUIDField): return lambda : provider.uuid()

        if isinstance(field, models.BooleanField): return lambda : self.fake.boolean()
        if isinstance(field, models.NullBooleanField): return lambda : self.fake.null_boolean()
        if isinstance(field, models.PositiveSmallIntegerField): return lambda : provider.rand_small_int(pos=True)
        if isinstance(field, models.SmallIntegerField): return lambda : provider.rand_small_int()
        if isinstance(field, models.BigIntegerField): return lambda : provider.rand_big_int()
        if isinstance(field, models.PositiveIntegerField): return lambda : provider.rand_small_int(pos=True)
        if isinstance(field, models.IntegerField): return lambda : provider.rand_small_int()
        if isinstance(field, models.FloatField): return lambda : provider.rand_float()
        if isinstance(field, models.DecimalField): return lambda : random.random()

        if isinstance(field, models.URLField): return lambda : self.fake.uri()
        if isinstance(field, models.SlugField): return lambda : self.fake.slug()
        if isinstance(field, models.IPAddressField) or isinstance(field, models.GenericIPAddressField):
            protocol = random.choice(['ipv4', 'ipv6'])
            return lambda : getattr(self.fake, protocol)()
        if isinstance(field, models.EmailField): return lambda : self.fake.email()
        if isinstance(field, models.CommaSeparatedIntegerField) or \
                (isinstance(field, models.CharField) and (validate_comma_separated_integer_list in field.validators)):
            return lambda : provider.comma_sep_ints()

        if isinstance(field, models.BinaryField): return lambda : provider.binary()
        if isinstance(field, models.ImageField): return lambda : provider.file_name()
        if isinstance(field, models.FilePathField): return lambda : provider.file_name()
        if isinstance(field, models.FileField): return lambda : provider.file_name()

        if isinstance(field, models.CharField):
            return lambda : self.fake.text(field.max_length) if field.max_length >= 5 else self.fake.word()
        if isinstance(field, models.TextField): return lambda : self.fake.text()

        if isinstance(field, models.DateTimeField):
            # format with timezone if it is active
            return lambda : _timezone_format(self.fake.date_time())
        if isinstance(field, models.DateField): return lambda : self.fake.date()
        if isinstance(field, models.TimeField): return lambda : self.fake.time()
        if isinstance(field, ArrayField):
            return lambda : [self.field_guess_format(field.base_field)]

        # TODO: This should be fine, but I can't find any models that I can use
        # in a simple test case.
        if hasattr(field, '_default_hint'): return lambda : field._default_hint[1]
        raise AttributeError(field)
