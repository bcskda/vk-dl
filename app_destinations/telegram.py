import json
import telethon
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from app_config import *
from . import Destination, register_destination


class TelegramDestination(Destination):
    def __init__(self):
        super(TelegramDestination, self).__init__()
        self._client = None
        self._channel = None

    def _do_auth(self):
        if 'proxy' in self._auth:
            self._client = TelegramClient(
                App_tg_name, App_tg_id, App_tg_hash,
                proxy=self._auth['proxy']
            )
        else:
            self._client = TelegramClient(
                App_tg_name, App_tg_id, App_tg_hash
            )
        self._client.connect()
        if self._client.is_user_authorized():
            return

        auth = dict()
        for key, value in self._auth.items():
            auth[key] = callable(value) and value() or value
            if key == 'phone_number':
                self._client.send_code_request(auth[key])
        try:
            self._client.sign_in(
                auth['phone_number'],
                auth['code']
            )
        except SessionPasswordNeededError:
            self._client.sign_in(
                password=auth['password']
            )

    def _setup_channel(self):
        channel_title = App_tg_channel_title.format(
            self._client.get_me().username
        )
        try:
            self._channel = self._client.get_entity(channel_title)
        except ValueError:
            self._client(telethon.functions.channels.CreateChannelRequest(
                title=channel_title,
                about=App_tg_channel_desc
            ))
            self._channel = self._client.get_entity(channel_title)
        self._client(telethon.functions.channels.JoinChannelRequest(
            self._channel
        ))
        self._client(telethon.functions.messages.SendMessageRequest(
            self._channel,
            '--------BEGIN ATTACHMENT SERIES--------'
        ))

    def upload(self, attach: dict):
        if not self._client:
            self._do_auth()
            self._setup_channel()
        self._client(telethon.functions.messages.SendMessageRequest(
            self._channel,
            json.dumps(attach)
        ))

    def logout(self):
        if self._client:
            self._client(telethon.functions.messages.SendMessageRequest(
                self._channel,
                '--------END ATTACHMENT SERIES--------'
            ))
            self._client.disconnect()


register_destination('telegram', TelegramDestination)
