import pandas as pd

def analyze_traffic(data):
    df = pd.DataFrame(data)
    summary = df.groupby('protocol').agg({
        'length': ['mean', 'sum'],
        'src_ip': 'nunique',
        'dst_ip': 'nunique'
    }).reset_index()
    return summary

def detect_anomalies(data):
    df = pd.DataFrame(data)
    # Simple example: flag packets larger than a threshold as anomalies
    anomalies = df[df['length'] > 1500]
    return anomalies
