from typing import Tuple, List, Dict


class Parser:
    def __init__(self):
        self.attachments = set()

    def _contains(self, att) -> bool:
        return frozenset(att) in self.attachments

    def parse(self, data: str) -> Tuple[List[Dict], Dict]:
        parsed, state = self.parse_impl(data)
        diff = list()
        for r in filter(lambda att: not self._contains(att), parsed):
            self.attachments.add(frozenset(r.items()))
            diff.append(r)
        return diff, state

    def set_params(self, *args, **kwargs):
        raise NotImplementedError

    def initial_state(self) -> Dict:
        raise NotImplementedError

    def parse_impl(self, data: str) -> Tuple[List[Dict], Dict]:
        raise NotImplementedError


parsers = dict()


def register_parser(name, parser_class):
    if name in parsers:
        raise KeyError(f'Duplicate parser register, name={name}')
    else:
        parsers[name] = parser_class


from .im import *
