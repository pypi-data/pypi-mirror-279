from .unit import get_unit_by_data


class Call:
    def __init__(self, ps, func, context):
        self.ps = ps
        self.func = func
        self.context = context

    def __call__(self, *args):
        return self.func.run(self.ps, self.context, *args)


class Func:
    def __init__(self, data):
        self.extend = True if data.get('extend') is None else data['extend']
        self.name = data.get('name')
        self.args = data.get('args') or []
        self.default = data.get('default') or {}
        self.units = [get_unit_by_data(d) for d in data.get('units') or []]
        self.cmd_info = data.get('cmd') or []

    def __hash__(self):
        return hash(self.name)

    def pkg_call(self, ps, context):
        return Call(ps, self, context)

    def run(self, ps, context, *args):
        if len(args) != len(self.args):
            raise Exception(f'Func args is not matched: {self.args}, {args}')
        kwargs = {arg: args[i] for i, arg in enumerate(self.args)}
        result = {**self.default, **(context if self.extend else {}), **kwargs}

        cache = {}
        for unit in self.units:
            data = unit.run(ps, self, result, cache)
            result.update(data)

        prompt_update = ps.get_module_attr(self.prompt_update)
        if prompt_update is not ps.EmptyValueMa:
            result = prompt_update(result)

        prompt_execute = ps.get_module_attr(self.prompt_execute)
        if prompt_execute is not ps.EmptyValueMa:
            prompt_execute(result)

    @property
    def prompt_execute(self):
        return f'prompt_execute_{self.name}'

    @property
    def prompt_update(self):
        return f'prompt_update_{self.name}'
