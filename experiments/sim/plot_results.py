#!/usr/bin/env python3
# plot_results.py
# Generates publication-ready figures from open Python-based SIL results
# Figures support evaluation of GNSS spoofing as a cyber-safety risk

import csv
import os
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# File locations
# -----------------------------
TS_FILE = "experiments/sim/results_timeseries.csv"
SUM_FILE = "experiments/sim/results_summary.csv"
OUT_DIR = "src/figures"   # paper-ready output directory

os.makedirs(OUT_DIR, exist_ok=True)

# -----------------------------
# Load time-series data
# -----------------------------
data = {}

if not os.path.exists(TS_FILE):
    raise FileNotFoundError(f"Missing time-series file: {TS_FILE}")

with open(TS_FILE, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        mag = float(row["mag"])
        trial = int(row["trial"])
        key = (mag, trial)
        if key not in data:
            data[key] = {
                "t": [], "x": [], "y": [],
                "gx": [], "gy": [], "res": []
            }
        data[key]["t"].append(float(row["t"]))
        data[key]["x"].append(float(row["true_x"]))
        data[key]["y"].append(float(row["true_y"]))
        data[key]["gx"].append(float(row["gnss_x"]))
        data[key]["gy"].append(float(row["gnss_y"]))
        data[key]["res"].append(float(row["residual"]))

# -----------------------------
# Choose representative trial
# -----------------------------
reps = {}
for (mag, trial) in sorted(data.keys()):
    if trial == 1:
        reps[mag] = data[(mag, trial)]

# -----------------------------
# Figure 1: Trajectory deviation
# -----------------------------
plt.figure(figsize=(6, 4))
for mag in [0.0, 30.0]:
    d = reps.get(mag)
    if d is None:
        continue

    plt.plot(
        d["x"], d["y"],
        label=f"True trajectory (mag={int(mag)} m)",
        linestyle="-" if mag == 0 else "--"
    )
    plt.plot(
        d["gx"], d["gy"],
        label=f"GNSS-reported trajectory (mag={int(mag)} m)",
        linestyle=":" if mag == 0 else "-."
    )

plt.xlabel("X position [m]")
plt.ylabel("Y position [m]")
plt.title("True vs GNSS-Reported Trajectories (SIL simulation)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig_trajectory_deviation.png"), dpi=300)

# -----------------------------
# Figure 2: Residual over time
# -----------------------------
plt.figure(figsize=(7, 3))
for mag, d in sorted(reps.items()):
    plt.plot(d["t"], d["res"], label=f"{int(mag)} m")

# Spoofing window markers
plt.axvline(10, color="gray", linestyle="--", linewidth=1)
plt.axvline(30, color="gray", linestyle="--", linewidth=1)

plt.xlabel("Time [s]")
plt.ylabel("Residual magnitude [m]")
plt.title("Residual Between GNSS Measurements and Navigation Filter Prediction")
plt.legend(title="Spoofing magnitude")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig_residual_time.png"), dpi=300)

# -----------------------------
# Figure 3: Max GNSS error distribution
# -----------------------------
maxes_by_mag = {}

if not os.path.exists(SUM_FILE):
    raise FileNotFoundError(f"Missing summary file: {SUM_FILE}")

with open(SUM_FILE, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        mag = float(row["mag"])
        val = float(row["max_gnss_error"])
        maxes_by_mag.setdefault(mag, []).append(val)

labels = [str(int(m)) for m in sorted(maxes_by_mag.keys())]
groups = [maxes_by_mag[m] for m in sorted(maxes_by_mag.keys())]

plt.figure(figsize=(6, 3))
plt.boxplot(groups, labels=labels, showfliers=True)
plt.xlabel("Spoofing magnitude [m]")
plt.ylabel("Maximum GNSS position error [m]")
plt.title("Maximum GNSS Error vs Spoofing Magnitude (SIL simulation)")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig_max_error_vs_spoofing.png"), dpi=300)

print(f"Figures successfully saved to '{OUT_DIR}'")
