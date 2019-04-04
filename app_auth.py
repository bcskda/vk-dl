import urllib.parse
from typing import List
import PyQt5.QtCore as Core
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import app_config


class Authorizer(Core.QObject):
    auth_success = Core.pyqtSignal(dict)
    auth_fail = Core.pyqtSignal(dict)

    def _is_auth_page(url: urllib.parse.SplitResult):
        if url.netloc != app_config.Auth_redir['netloc']:
            return False
        elif url.path != app_config.Auth_redir['path']:
            return False
        else:
            return True

    def __init__(self, parent: QWidget = None):
        super(Authorizer, self).__init__(parent)

    @Core.pyqtSlot(QWebEngineView, List[str], name='auth_in_view')
    def auth_in_view(self, view: QWebEngineView, permissions):
        self._view = view
        view.urlChanged.connect(self.on_post_auth_redirect)
        view.load(Core.QUrl(app_config.make_auth_url(permissions)))
        view.show()

    @Core.pyqtSlot(Core.QUrl, name='on_post_auth_redirect')
    def on_post_auth_redirect(self, url: Core.QUrl):
        url = urllib.parse.urlsplit(url.toString())
        if Authorizer._is_auth_page(url):
            self._view.urlChanged.disconnect(self.on_post_auth_redirect)
            auth_result = url.fragment.split('&')
            auth_result = dict(map(lambda p: tuple(p.split('=')), auth_result))
            if 'auth_token' in auth_result:
                signal = self.auth_success
            else:
                signal = self.auth_fail
            signal.emit(auth_result)
