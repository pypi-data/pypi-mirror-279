import scapy.all as scapy

def capture_packets(interface, count):
    packets = scapy.sniff(iface=interface, count=count)
    return packets

def parse_packet(packet):
    return {
        'src_ip': packet[scapy.IP].src,
        'dst_ip': packet[scapy.IP].dst,
        'protocol': packet[scapy.IP].proto,
        'length': len(packet)
    }

def collect_data(interface, count):
    packets = capture_packets(interface, count)
    parsed_data = [parse_packet(packet) for packet in packets]
    return parsed_data
