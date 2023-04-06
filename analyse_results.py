import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

results = pd.read_csv("full_results.csv")

bitrates = list(range(1, 36))
latencies = []
jitters = []
for i in bitrates:
    col = results[f"test_1080p50-H264-{i}M.mp4"].dropna().to_numpy()
    latencies.append(np.average(col))
    jitters.append(np.max(col)-np.min(col))


plt.subplot(121)
plt.title("System latency: 1080p50 h264")
plt.plot(bitrates, latencies)
plt.xlabel("Video bitrate (Mbps)")
plt.ylabel("Latency (frames @ 50fps)")

plt.subplot(122)
plt.plot(bitrates, jitters)
plt.title("System jitter: 1080p50 h264")
plt.xlabel("Video bitrate (Mbps)")
plt.ylabel("Jitter (frames @ 50fps)")

plt.show()