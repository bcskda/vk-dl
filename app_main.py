import sys
import json
# import PyQt5.QtGui as Gui
import PyQt5.QtCore as Core
from PyQt5.QtWidgets import QApplication  # , QPlainTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
import app_extractor
import app_auth


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

        self.authorizer.auth_success.connect(self.on_auth_result)
        self.authorizer.auth_fail.connect(self.on_auth_result)
        # self.authorizer.auth_in_view.connect("""!!!<some button on_click here>!!!""")

        self.extractor.on_data.connect(self.on_extract_data)
        self.extractor.on_finish.connect(self.on_extract_finish)

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
        self.attachments.append(attachments)
        # ls = map(json.dumps, ls)
        # self.text_view.show()
        # doc = Gui.QTextDocument(self.text_view)
        # doc.setPlainText('\n'.join(ls))
        # self.text_view.setDocument(doc)

    @Core.pyqtSlot(name='on_extract_finish')
    def on_extract_finish(self):
        print('MainApplication: transmission finished')
        with open('im_photos.json', 'w') as out:
            print(json.dumps(self.attachments), file=out)


def main():
    app = MainAppliction(sys.argv)
    app.authorizer.auth_in_view(app.web_view, 'friends')
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
