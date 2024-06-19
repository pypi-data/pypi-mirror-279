import unittest
from netmonitor import visualization
import pandas as pd

class TestVisualization(unittest.TestCase):

    def test_plot_traffic_summary(self):
        # Create a sample summary DataFrame for testing
        summary = pd.DataFrame({
            'protocol': [6, 17],
            'length': {
                'mean': [150.0, 100.0],
                'sum': [300, 200]
            },
            'src_ip': [2, 1],
            'dst_ip': [2, 1]
        })

        try:
            visualization.plot_traffic_summary(summary)
        except Exception as e:
            self.fail(f"plot_traffic_summary raised an exception: {e}")

    def test_plot_anomalies(self):
        # Create a sample anomalies DataFrame for testing
        anomalies = pd.DataFrame({
            'length': [1600, 2000],
            'index': [1, 2]
        })

        try:
            visualization.plot_anomalies(anomalies)
        except Exception as e:
            self.fail(f"plot_anomalies raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
