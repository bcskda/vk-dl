import sys
import json
# import PyQt5.QtGui as Gui
import PyQt5.QtCore as Core
from PyQt5.QtWidgets import QApplication  # , QPlainTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
import app_extractor
import app_auth
import app_destinations
import app_config


class MainAppliction(QApplication):
    def __init__(self, *argv):
        print('Raw cmdline:', argv)
        super(MainAppliction, self).__init__(*argv)

        self.args = {'source': argv[0][1]}
        params = map(lambda pair: tuple(pair.split(':')), argv[0][2:])
        params = list(params)
        print('Params:', params)
        self.args['params'] = dict(params)
        print('Command-line:', self.args)

        self.web_view = QWebEngineView()
        self.authorizer = app_auth.Authorizer()
        self.extractor = app_extractor.Extractor()
        self.destination = app_destinations.destinations['local']()

        self.authorizer.auth_success.connect(self.on_auth_result)
        self.authorizer.auth_fail.connect(self.on_auth_result)
        # self.authorizer.auth_in_view.connect("""!!!<some button on_click here>!!!""")

        self.extractor.on_data.connect(self.on_extract_data)
        self.extractor.on_finish.connect(self.on_extract_finish)

        self.destination.auth({'dest_file': app_config.local_filename_templ})

        self.attachments = []

    @Core.pyqtSlot(dict, name='on_auth_result')
    def on_auth_result(self, result: dict):
        print(f'Received auth result: {result}')
        self.extractor.set_source(self.args['source'])
        self.extractor.set_parser_params(**self.args['params'])
        self.extractor.execute_in_view(self.web_view)

    @Core.pyqtSlot(list, name='on_extract_data')
    def on_extract_data(self, attachments: list):
        print('MainApplication: received more {}'.format(len(attachments)))
        self.attachments.extend(attachments)
        # ls = map(json.dumps, ls)
        # self.text_view.show()
        # doc = Gui.QTextDocument(self.text_view)
        # doc.setPlainText('\n'.join(ls))
        # self.text_view.setDocument(doc)

    @Core.pyqtSlot(name='on_extract_finish')
    def on_extract_finish(self):
        print('MainApplication: list transmission finished')
        try:
            del self.web_view
        except Exception as e:
            print('MainActivity: Exception while deleting web_view:', e)
        with open('dest/im_photos.json', 'w') as out:
            print(json.dumps(self.attachments), file=out)
        for attach in self.attachments:
            self.destination.upload(attach)
        print('MainApplication: all files saved')


def main():
    app = MainAppliction(sys.argv)
    app.authorizer.auth_in_view(app.web_view, 'friends')
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
