from copy import deepcopy
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from prompt_toolkit.keys import Keys


def normalize_prompt(kwargs):
    result = deepcopy(kwargs)
    if kwargs['type'] == 'list':
        result['choices'] = dc = []
        choices = kwargs.get('choices') or []
        for choice in choices:
            if isinstance(choice, dict):
                dc.append(Choice(**choice))
            elif isinstance(choice, str):
                dc.append(choice)
            else:
                dc.append(Separator())

    if kwargs['type'] == 'input':
        if kwargs.get('multiline'):
            result.update({
                'keybindings': {
                    "answer": [
                        {"key": [Keys.End], "filter": True}
                    ],
                },
                'long_instruction': ' Press End to finish input',
                'instruction': ' Press End to finish input'
            })

    return result
