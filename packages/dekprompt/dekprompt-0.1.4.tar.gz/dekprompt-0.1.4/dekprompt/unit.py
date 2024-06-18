import os
from copy import deepcopy
from InquirerPy import prompt
from dektools.expression import eval_safe
from .utils import normalize_prompt

all_units = set()


def get_unit_by_data(data):
    unit_cls = get_unit_cls_by_type(data['type'])
    return unit_cls(data)


def get_unit_cls_by_type(typed):
    for unit in all_units:
        if typed in unit.types:
            return unit


class UnitMeta(type):
    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)
        if not new_class.__dict__.get('abstract'):
            all_units.add(new_class)
        return new_class


class UnitBase(metaclass=UnitMeta):
    abstract = True
    types = set()

    def __init__(self, data):
        self.data_kwargs = deepcopy(data)

    def run(self, ps, func, context, cache):
        condition = self.data_kwargs.get('if')
        if not condition or self.get_condition_boolean(context, condition):
            return self.on_run(ps, func, context, cache) or {}
        else:
            return {}

    def on_run(self, ps, func, context, cache):
        return {}

    @staticmethod
    def get_condition_boolean(context, expression):
        func = f"lambda _: {expression}"
        ev, errors = eval_safe(func)
        if errors:
            raise Exception(f'expression eval failed: [{errors}]')
        else:
            return ev()(type('condition', (object,), context))


class UnitPrompt(UnitBase):
    types = {'input', 'password', 'filepath', 'number', 'confirm', 'list', 'rawlist', 'fuzzy'}

    def on_run(self, ps, func, context, cache):
        kwargs = self.normalize_prompt(ps, func, self.data_kwargs)
        rd = prompt(questions=[kwargs])
        key = kwargs.get('name')
        result = rd[key] if key else rd[0]
        name = self.data_kwargs.get('name')
        if name:
            return {name: result}
        else:
            return {}

    @staticmethod
    def normalize_prompt(ps, func, kwargs):
        result = normalize_prompt(kwargs)

        # https://inquirerpy.readthedocs.io/en/latest/pages/dynamic.html
        for attr in ('transformer', 'validate', 'filter', 'default'):
            key = kwargs.get("name")
            if key:
                ma = ps.get_module_attr(f'prompt_{attr}_{func.name}_{key}')
                if ma is not ps.EmptyValueMa:
                    result[attr] = ma

        return result


class UnitWorkdir(UnitBase):
    types = {'wd'}

    def on_run(self, ps, func, context, cache):
        wd = self.data_kwargs.get('wd')
        if wd:
            wd = wd.format(**context)
            os.chdir(wd)
            lst = cache.setdefault('wd', [])
            lst.append(os.getcwd())
        else:
            lst = cache['wd']
            os.chdir(lst.pop())


class UnitCommand(UnitBase):
    types = {'cmd'}

    def on_run(self, ps, func, context, cache):
        cmd = self.data_kwargs.get('cmd')
        if cmd:
            self.run_cmd_list(cmd, context)

    @classmethod
    def run_cmd_list(cls, cmd_info, data):
        if isinstance(cmd_info, str):
            cmd_info = cmd_info.format(**data)
            for cmd in cmd_info.split('\n'):
                cmd = cmd.strip()
                if cmd:
                    os.system(cmd)
            return
        elif isinstance(cmd_info, list):
            cls.run_cmd_list('\n'.join(cmd_info), data)
            return
        elif isinstance(cmd_info, dict):
            array = []
            for key, cmd in cmd_info.items():
                if data.get(key):
                    array.append(cmd)
            cls.run_cmd_list(array, data)
            return
        raise Exception(f'unknown command: {cmd_info}')


class UnitCall(UnitBase):
    types = {'call'}

    def on_run(self, ps, func, context, cache):
        cb = self.data_kwargs.get('call')
        if cb:
            cb = cb.format(**context)
            ev, errors = eval_safe(cb, glo={
                **{k: f.pkg_call(ps, context) for k, f in ps.func_map.items()},
                **context})
            if errors:
                raise Exception(f'eval_safe: {errors}')
            else:
                ev()


class UnitExec(UnitBase):
    types = {'exec'}

    def on_run(self, ps, func, context, cache):
        name = self.data_kwargs.get('name') or func.name
        for attr in [
            f'prompt_update_{name}',
            f'prompt_exec_{name}'
        ]:
            prompt_attr = ps.get_module_attr(attr)
            if prompt_attr is not ps.EmptyValueMa:
                prompt_attr(context)
