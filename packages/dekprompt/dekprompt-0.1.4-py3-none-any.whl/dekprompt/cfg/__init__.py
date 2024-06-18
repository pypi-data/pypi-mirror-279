import os
from collections import OrderedDict
from InquirerPy import prompt
from dektools.yaml import yaml
from dektools.dict import is_dict, dict_merge
from dektools.shell import shell_output
from ..utils import normalize_prompt


class Cfg:
    _empty_value = object()

    @classmethod
    def _get_value(cls, values, keys):
        cursor = values
        for key in keys:
            if key not in cursor:
                return cls._empty_value
            cursor = cursor[key]
        return cursor

    def inputs_update_cfg(self, values, schema_list):
        questions = []
        types = {}
        for keys, meta in schema_list:
            default = self._get_value(values, keys)
            if default is self._empty_value:
                shell = meta.get('shell')
                if shell:
                    default = shell_output(shell)
                else:
                    default = meta["default"]
            if default is None:
                default = ''
            name = '.'.join(keys)
            types[name] = default.__class__
            questions.append(normalize_prompt({
                "type": meta.get("type", "input"),
                "message": name + ":",
                "name": name,
                "default": str(default)
            }))
        inputs = prompt(questions)
        result = OrderedDict()
        for keys, _ in schema_list:
            cursor = result
            for key in keys[:-1]:
                cursor = cursor.setdefault(key, OrderedDict())
            name = '.'.join(keys)
            cursor[keys[-1]] = types[name](inputs[name])
        return result


class CfgFile(Cfg):
    marker_meta = '__meta__'

    def __init__(self, path_cfg, *paths_schema):
        self.path_cfg = path_cfg
        self.paths_schema = paths_schema

    @classmethod
    def _flat_schema(cls, schema, *keys):
        result = []
        for k, v in schema.items():
            if k.endswith(cls.marker_meta):
                continue
            km = k + cls.marker_meta
            if km in schema or not is_dict(v):
                result.append(((*keys, k), {'default': v} | (schema.get(km) or {})))
            else:
                result.extend(cls._flat_schema(v, *keys, k))

        return result

    @property
    def values(self):
        if self.path_cfg and os.path.isfile(self.path_cfg):
            return yaml.load(self.path_cfg)
        else:
            return OrderedDict()

    @property
    def schema(self):
        schema = OrderedDict()
        for path_schema in self.paths_schema:
            dict_merge(schema, yaml.load(path_schema))
        return self._flat_schema(schema)

    def apply(self):
        result = self.inputs_update_cfg(self.values, self.schema)
        if self.path_cfg:
            yaml.dump(self.path_cfg, result)
        return result
