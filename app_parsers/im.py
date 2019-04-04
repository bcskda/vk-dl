from typing import Tuple, List, Dict
from app_parsers import Parser, register_parser
import app_regex
import app_config


class ImParser(Parser):
    def __init__(self):
        super(ImParser, self).__init__()
        self.peer = None

    def set_params(self, peer: str, *args, **kwargs):
        self.peer = peer

    def initial_state(self) -> Dict:
        default_args = {'peer_id': self.peer, 'from_id': None}
        return {'args': default_args, 'finished': False}

    def parse_impl(self, html: str) -> Tuple[List[Dict], Dict]:
        next_from = app_regex.ex_next_from.search(html)
        if not next_from:
            return [], {'finished': True}
        next_from = next_from.group(1)

        attachments = list()
        for match_att in app_regex.ex_attachment.finditer(html):
            att = dict()
            att['id'] = app_regex.ex_id.search(match_att.group(0)).group(1)
            att['date'] = app_regex.ex_date.search(match_att.group(0)).group(1)

            sizes = dict(app_regex.ex_size.findall(match_att.group(0)))
            for sz in app_config.photo_size_priority:
                if sz in sizes:
                    att['url'] = sizes[sz]
                    break

            attachments.append(att)
        next_args = {'peer_id': self.peer, 'from_id': next_from}
        return attachments, {'args': next_args, 'finished': False}


register_parser('im', ImParser)
