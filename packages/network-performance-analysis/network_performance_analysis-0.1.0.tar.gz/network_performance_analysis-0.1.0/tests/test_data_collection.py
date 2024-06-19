import unittest
from netmonitor import data_collection

class TestDataCollection(unittest.TestCase):

    def test_parse_packet(self):
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

        packet = MockPacket()
        parsed = data_collection.parse_packet(packet)
        self.assertEqual(parsed['src_ip'], '192.168.1.1')
        self.assertEqual(parsed['dst_ip'], '192.168.1.2')
        self.assertEqual(parsed['protocol'], 6)
        self.assertEqual(parsed['length'], len(packet))

if __name__ == '__main__':
    unittest.main()
