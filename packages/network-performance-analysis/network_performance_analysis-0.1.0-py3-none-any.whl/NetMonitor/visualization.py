import matplotlib.pyplot as plt

def plot_traffic_summary(summary):
    summary.plot(kind='bar', x='protocol', y=('length', 'sum'), legend=False)
    plt.title('Traffic Summary by Protocol')
    plt.xlabel('Protocol')
    plt.ylabel('Total Length')
    plt.show()

def plot_anomalies(anomalies):
    plt.scatter(anomalies.index, anomalies['length'])
    plt.title('Anomalies in Traffic')
    plt.xlabel('Packet Index')
    plt.ylabel('Packet Length')
    plt.show()
