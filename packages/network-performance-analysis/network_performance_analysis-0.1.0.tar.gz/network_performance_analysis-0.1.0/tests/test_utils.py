import unittest
from netmonitor import utils
import scapy.all as scapy

class TestUtils(unittest.TestCase):

    def test_get_interface_list(self):
        interfaces = utils.get_interface_list()
        self.assertIsInstance(interfaces, list)

    def test_validate_ip_address(self):
        self.assertTrue(utils.validate_ip_address('192.168.1.1'))
        self.assertFalse(utils.validate_ip_address('invalid_ip'))

    def test_convert_protocol_number_to_name(self):
        self.assertEqual(utils.convert_protocol_number_to_name(6), 'TCP')
        self.assertEqual(utils.convert_protocol_number_to_name(17), 'UDP')
        self.assertEqual(utils.convert_protocol_number_to_name(999), 'Unknown')

    def test_get_packet_summary(self):
        # Create a mock packet for testing
        class MockPacket:
            def __init__(self):
                self[scapy.IP] = self

            @property
            def src(self):
                return '192.168.1.1'

            @property
            def dst(self):
                return '192.168.1.2'

            @property
            def proto(self):
                return 6  # TCP

            def __len__(self):
                return 100

        packet = MockPacket()
        summary = utils.get_packet_summary(packet)
        self.assertEqual(summary, '192.168.1.1 -> 192.168.1.2 (TCP)')

if __name__ == '__main__':
    unittest.main()
