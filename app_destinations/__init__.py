class Destination:
    def __init__(self):
        super(Destination, self).__init__()
        self._auth = None

    def auth(self, auth_data: dict):
        self._auth = auth_data

    def upload(self, attachment: dict):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

    def __del__(self):
        self.logout()


destinations = dict()


def register_destination(name, cls):
    if name in destinations:
        raise KeyError(f'Duplicate parser register, name={name}')
    else:
        destinations[name] = cls


from . import local
from . import telegram
