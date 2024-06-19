# Importing modules to make them accessible directly from the package
from .data_collection import capture_packets, parse_packet, collect_data
from .data_analysis import analyze_traffic, detect_anomalies
from .visualization import plot_traffic_summary, plot_anomalies
from .utils import get_interface_list, validate_ip_address, convert_protocol_number_to_name, get_packet_summary

# Define the version of our package
__version__ = '0.1.0'
