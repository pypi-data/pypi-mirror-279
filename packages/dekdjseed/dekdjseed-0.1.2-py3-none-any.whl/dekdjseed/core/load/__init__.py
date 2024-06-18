import re
import importlib
from pathlib import Path
from dektools.yaml import load_yaml
from dektools.dict import assign


class SeedException(Exception):
    pass


class EmptyValue:
    pass


class SeedLoader:
    EMPTY_VALUE = EmptyValue()
    seed_prefix = 'seed_'
    settings_filename = 'settings.yaml'
    default_seed = 'dekdjseed.core.seed'
    default_settings = dict(
        config=dict(number=10),
        models=[]
    )

    @classmethod
    def from_module(cls, module, guesser):
        def take_seeds(m):
            result = {}
            for k, v in vars(m).items():
                if k.startswith(cls.seed_prefix) and callable(v):
                    result[k[len(cls.seed_prefix):]] = v
            return result

        try:
            module_seed = importlib.import_module(module)
            filepath = Path(module_seed.__file__).parent / cls.settings_filename
        except ModuleNotFoundError:
            module_seed = None
            filepath = None
        return cls(
            guesser,
            assign(
                load_yaml(Path(__file__).parent / cls.settings_filename),
                load_yaml(filepath) if filepath else {},
            ),
            assign(
                take_seeds(importlib.import_module(cls.default_seed)),
                take_seeds(module_seed) if module_seed else {}
            )
        )

    def __init__(self, guesser, settings, seed_funcs=None):
        self.guesser = guesser
        self.seed_funcs = seed_funcs or {}
        self.models = {}
        self._parse(settings)

    def _parse(self, settings):
        def transform_value(value):
            if isinstance(value, str):
                match = re.match(r'\$([a-zA-z_0-9]+)([(]*[\S\s]*[)]*)', value)
                if match:
                    func_name, args = match.groups()
                    func = self.seed_funcs.get(func_name)
                    if not func:
                        raise SeedException(f'Can not find func [{func_name}]')
                    try:
                        args = list(eval(args)) if args else []
                    except SyntaxError:
                        raise SeedException(f'SyntaxError [{value}] when eval [{args}]')
                    return lambda *x: func(args, self.guesser, *x)
            return value

        for name, model_config in settings['models'].items():
            self.models[name] = dict(
                config={key: transform_value(value) for key, value in model_config.get('config', {}).items()},
                fields={key: transform_value(value) for key, value in model_config.get('fields', {}).items()}
            )

    def get_model(self, model_cls):
        result = dict()
        for cls in reversed(model_cls.mro()):
            result = assign(result, self.models.get(cls.__name__, {}))
        return result

    def get_model_config_value(self, model_cls, config_key, *args):
        return self.get_model_value(model_cls, ['config', config_key], *args)

    def get_model_field_value(self, model_cls, field_name, *args):
        return self.get_model_value(model_cls, ['fields', field_name], *args)

    def get_model_value(self, model_cls, keys, *args):
        item = self.get_model(model_cls)
        if item:
            cursor = item
            for key in keys[:-1]:
                cursor = cursor.get(key, {})
            value = cursor.get(keys[-1], self.EMPTY_VALUE)
            if value is not self.EMPTY_VALUE:
                if callable(value):
                    return value(*args)
                return value
        return self.EMPTY_VALUE
