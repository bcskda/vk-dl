import os.path
import requests
import time
from . import Destination, register_destination


class LocalDestination(Destination):
    def upload(self, attach: dict):
        rq = requests.get(attach['url'])
        if not rq.ok:
            return False, rq.status_code
        else:
            basename = os.path.basename(attach['url'])
            dt = time.gmtime(int(attach['date']))
            dt = time.strftime('%Y-%m-%d_%H:%M:%S_%z', dt)
            filename = self._auth['dest_file'].format(dt, basename)
            with open(filename, 'wb') as out:
                out.write(rq.content)
            return True, filename

    def logout(self):
        pass


register_destination('local', LocalDestination)
