from unittest import TestCase
from .local import LocalDestination
from app_config import local_filename_templ


class TestLocalDestination(TestCase):
    destination: LocalDestination = LocalDestination()

    def test_upload(self):
        attach = dict()
        attach['id'] = '456245531'
        attach['date'] = '1552174102'
        attach['url'] = 'https://pp.userapi.com/c834403/v834403065/f8185/IfW2EhIpFPQ.jpg'
        self.destination.auth({'dest_file': local_filename_templ})
        ok, result = self.destination.upload(attach)

        expected_filename = '2019-03-09_23:28:22_+0000_IfW2EhIpFPQ.jpg'
        self.assertTrue(ok)
        self.assertEqual(expected_filename, result)
