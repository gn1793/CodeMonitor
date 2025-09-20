import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def main(csv_path="codemonitor.csv", out_png="codemonitor_plot.png"):
    df = pd.read_csv(csv_path)
    if "ts_ms" not in df.columns:
        raise SystemExit("ts_ms column missing")
    df["t"] = (df["ts_ms"] - df["ts_ms"].min()) / 1000.0

    plt.figure()
    df.plot(x="t", y=["cpu_pct", "ram_pct"], ax=plt.gca())
    plt.xlabel("time (s)")
    plt.ylabel("percent")
    plt.title("CPU & RAM over time")
    plt.tight_layout()
    plt.savefig(out_png)
    print("Saved", out_png)

if __name__ == "__main__":
    main()
