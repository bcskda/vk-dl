import json
import functools
from typing import List, Dict
import PyQt5.QtCore as Core
from PyQt5.QtWebEngineWidgets import QWebEngineScript, QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
import app_config
import app_parsers


class Receiver(Core.QObject):
    """Receives data from WebChannel through slot"""

    get_next_series = Core.pyqtSignal(str, name='get_next_series')
    on_data = Core.pyqtSignal(list)
    on_finish = Core.pyqtSignal()

    def __init__(self, parent: Core.QObject = None):
        super(Receiver, self).__init__(parent)
        self.parser = None

    def set_source(self, source: str):
        try:
            self.parser = app_parsers.parsers[source]()
        except KeyError:
            raise Exception(f'No parser for source {source}')

    def set_parser_params(self, *args, **kwargs):
        self.parser.set_params(*args, **kwargs)

    @Core.pyqtSlot(str, name='init')
    def on_init_exchange(self, mesg: str):
        """Called by injected js when ready to communicate"""
        print(f'Receiver: Initiate from injection: {mesg}')
        print('Parser: {}; {}'.format(self.parser.__class__, dir(self.parser)))
        initial_args = self.parser.initial_state()['args']
        self.get_next_series.emit(json.dumps(initial_args))

    @Core.pyqtSlot(str, name='on_dev_result')
    def on_dev_result(self, html: str):
        """Called by injected js when another series becomes available"""
        # print('Received series from injection')
        attachments, state = self.parser.parse(html)
        if not state['finished']:
            self.on_data.emit(attachments)
            self.get_next_series.emit(json.dumps(state['args']))
        else:
            print('Receiver: Finished')
            self.on_finish.emit()

    @Core.pyqtSlot(str, str, name='log')
    def on_js_log(self, mesg: str, data: str):
        print('LOG JS "{}": {}'.format(mesg, data))


@functools.lru_cache(maxsize=1)
def _get_jsinject_dep_code():
    """Return Qt's js required for WebChannel scripting"""

    file = Core.QFile(app_config.jsinject_dep)
    file.open(Core.QIODevice.ReadOnly)
    return bytes(file.readAll()).decode('utf-8')


class Extractor(Core.QObject):
    on_data = Core.pyqtSignal(list)
    on_finish = Core.pyqtSignal()

    @Core.pyqtSlot(list, name='on_recv_data')
    def _on_recv_data(self, attachments: list):
        self.on_data.emit(attachments)

    @Core.pyqtSlot(name='on_recv_finish')
    def _on_recv_finish(self):
        self.on_finish.emit()

    def __init__(self, parent=None):
        super(Extractor, self).__init__(parent)
        self.url = None
        self.jscode = None
        self.receiver = Receiver(parent)

        self.receiver.on_data.connect(self._on_recv_data)
        self.receiver.on_finish.connect(self._on_recv_finish)

    def set_source(self, source: str):
        try:
            self.url = app_config.source_url[source]
            self.jscode = app_config.jsinject_code[source]
            self.receiver.set_source(source)
        except KeyError:
            raise KeyError(f'No url/injection for source {source}')

    def set_parser_params(self, *source_args, **source_kwargs):
        self.receiver.set_parser_params(*source_args, **source_kwargs)

    def execute_in_view(self, view: QWebEngineView):
        view.load(Core.QUrl(self.url))
        page = view.page()

        channel = QWebChannel(view)
        page.setWebChannel(channel)
        channel.registerObject('app_receiver', self.receiver)

        script = QWebEngineScript()
        script.setSourceCode(_get_jsinject_dep_code() + self.jscode)
        script.setWorldId(QWebEngineScript.MainWorld)
        page.profile().scripts().insert(script)
