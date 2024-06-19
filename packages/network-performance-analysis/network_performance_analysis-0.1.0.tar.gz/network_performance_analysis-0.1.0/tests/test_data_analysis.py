import unittest
from netmonitor import data_analysis

class TestDataAnalysis(unittest.TestCase):

    def test_analyze_traffic(self):
        data = [
            {'protocol': 6, 'length': 100, 'src_ip': '192.168.1.1', 'dst_ip': '192.168.1.2'},
            {'protocol': 6, 'length': 200, 'src_ip': '192.168.1.3', 'dst_ip': '192.168.1.4'},
            {'protocol': 17, 'length': 150, 'src_ip': '192.168.1.5', 'dst_ip': '192.168.1.6'}
        ]
        summary = data_analysis.analyze_traffic(data)
        self.assertEqual(len(summary), 2)

    def test_detect_anomalies(self):
        data = [
            {'protocol': 6, 'length': 100},
            {'protocol': 6, 'length': 2000},  # This should be flagged as an anomaly
            {'protocol': 17, 'length': 150}
        ]
        anomalies = data_analysis.detect_anomalies(data)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies.iloc[0]['length'], 2000)

if __name__ == '__main__':
    unittest.main()
