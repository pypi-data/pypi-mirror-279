import os
import json
from pathlib import Path
from importlib import import_module
from dektools.yaml import yaml
from .func import Func


class Prompt:
    EmptyValueMa = object()
    config_files_ext = ['.json', '.yaml', '.yml']

    def __init__(self, module):
        self.module = import_module(module) if isinstance(module, str) else module
        self.func_map = {}
        self.entry = None
        self.setup()

    def setup(self):
        self.load_config_files()

    @property
    def module_dir(self):
        return str(Path(self.module.__file__).resolve().parent)

    def get_func(self, func_name):
        return self.func_map.get(func_name)

    def get_module_attr(self, name):
        return getattr(self.module, name, self.EmptyValueMa)

    def load_config_file(self, data):
        prompt = data.get('prompt') or {}
        entry = prompt.get('entry') or None
        if entry:
            self.entry = entry
        for defined in prompt.get('def') or []:
            func = Func(defined)
            self.func_map[func.name] = func

    def load_config_files(self):
        for file in sorted(os.listdir(self.module_dir)):
            filepath = Path(self.module_dir) / file
            if os.path.isfile(filepath) and os.path.splitext(filepath)[-1] in self.config_files_ext:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    data = {}
                    ext = os.path.splitext(filepath)[-1]
                    if ext in ['.yaml', 'yml']:
                        data = yaml.loads(content)
                    elif ext in ['.json']:
                        data = json.loads(content)
                    self.load_config_file(data)


class PromptSet:
    EmptyValueMa = Prompt.EmptyValueMa

    @classmethod
    def from_modules(cls, *modules):
        return cls(*[Prompt(module) for module in modules])

    def __init__(self, *prompt_list):
        self.prompt_list = prompt_list
        self.func_map = {}
        self.setup()

    def setup(self):
        for prompt in self.prompt_list:
            self.func_map.update(prompt.func_map)

    def run(self):
        entry = self.get_entry()
        if not entry:
            raise Exception('Can not find a entry')
        self.run_func(self.get_func(entry))

    def run_func(self, func, *args):
        func.run(self, {}, *args)

    def get_entry(self):
        for prompt in reversed(self.prompt_list):
            if prompt.entry:
                return prompt.entry

    def get_func(self, func_name):
        return self.func_map.get(func_name)

    def get_module_attr(self, attr_name):
        for prompt in self.prompt_list:
            attr = prompt.get_module_attr(attr_name)
            if attr is not Prompt.EmptyValueMa:
                return attr
        return self.EmptyValueMa
