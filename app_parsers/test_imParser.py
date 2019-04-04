from unittest import TestCase
import app_parsers


class TestImParser(TestCase):
    parser: app_parsers.ImParser = app_parsers.parsers['im']()

    def test_set_peer(self):
        self.parser.set_params(peer='0')
        self.assertEqual(self.parser.peer, '0')

    def test_initial_state(self):
        expected_args = {'peer_id': self.parser.peer, 'from_id': None}
        expected_state = {'args': expected_args, 'finished': False}
        state = self.parser.initial_state()
        self.assertEqual(state, expected_state)

    def test_on_data(self):
        with open('../tests/dev_result_im.html') as input:
            html = input.read()
            result, state = self.parser.parse_impl(html)
            self.assertEqual(len(result), 10)
