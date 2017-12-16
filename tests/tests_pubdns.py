import unittest
import pubdns
from mock import patch

class TestPubDNS(unittest.TestCase):
    """ test pubdns class methods """
    def test_get_data(self):
        """ test _get_data exception """
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 400
            pd = pubdns.PubDNS.__new__(pubdns.PubDNS)
            with self.assertRaises(Exception):
                pd._get_data()