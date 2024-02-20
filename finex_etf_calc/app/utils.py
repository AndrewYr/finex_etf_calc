import os
import inspect
from distutils.util import strtobool

from ruamel.yaml import YAML

yaml_loader = YAML(typ='safe')


class MagConfig:

    @staticmethod
    def _to_bool(value):
        if isinstance(value, bool):
            return value
        return bool(strtobool(value))

    @staticmethod
    def _merge_dicts(*dicts):
        return {k: v for d in dicts if d for k, v in d.items()}

    @classmethod
    def _get_value(cls, attr, attr_type, attrs_info, params):
        raw_value = params.get(attr, attrs_info.get(attr))
        converter = cls._to_bool if attr_type is bool else attr_type
        return converter(raw_value) if raw_value is not None else None

    def _get_annotations(self):
        return {k: v for cls in inspect.getmro(type(self)) for k, v in getattr(cls, '__annotations__', {}).items()}

    def __init__(self, params: dict):
        self._params = params
        annotations = self._get_annotations()
        info = {k: v for k, v in inspect.getmembers(type(self)) if not k.startswith('_') and not callable(v)}

        for attr, attr_type in annotations.items():
            if attr not in info or not isinstance(info[attr], property):
                try:
                    value = self._get_value(attr, attr_type, info, params)
                    setattr(self, attr, value)
                except Exception as ex:
                    raise ValueError(f'Unable to parse value for attribute {attr}. All values: {params}') from ex

        for attr, value in info.items():
            if attr not in annotations and not isinstance(value, property):
                setattr(self, attr, params.get(attr, value))

    @classmethod
    def from_file(cls, filename, loader=yaml_loader) -> 'MagConfig':
        with open(filename) as f:
            raw_data = loader.load(f)

        prepared_dict = cls._merge_dicts(raw_data, os.environ)
        return cls(prepared_dict)
