#!/usr/bin/env python3
# simple_evtol_sim.py
# Open, reproducible Python-based SIL simulation for evaluating
# GNSS spoofing as a cyber-safety risk during low-altitude eVTOL operations

import csv
import numpy as np
import random
import os

# =========================================================
# Reproducibility
# =========================================================
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# =========================================================
# Simulation parameters
# =========================================================
DT = 0.1                 # time step [s]
T_TOTAL = 60.0           # total simulation time [s]
ATTACK_START = 10.0      # spoof start time [s]
ATTACK_END = 30.0        # spoof end time [s]

GNSS_SIGMA = 0.3         # GNSS measurement noise [m]
PRED_SIGMA = 0.5         # navigation prediction uncertainty [m]

SPOOF_MAGNITUDES = [0.0, 10.0, 30.0, 60.0]
N_TRIALS = 5
DETECTION_THRESHOLD = 3.0  # residual threshold [m]

# =========================================================
# Output paths
# =========================================================
OUT_DIR = "experiments/sim"
TS_FILE = os.path.join(OUT_DIR, "results_timeseries.csv")
SUM_FILE = os.path.join(OUT_DIR, "results_summary.csv")

os.makedirs(OUT_DIR, exist_ok=True)

# =========================================================
# Open CSV files
# =========================================================
ts_f = open(TS_FILE, "w", newline="")
sum_f = open(SUM_FILE, "w", newline="")

ts_writer = csv.writer(ts_f)
sum_writer = csv.writer(sum_f)

# ---------------------------------------------------------
# CSV headers
# ---------------------------------------------------------
ts_writer.writerow([
    "seed", "mag", "trial", "t",
    "true_x", "true_y",
    "gnss_x", "gnss_y",
    "residual"
])

sum_writer.writerow([
    "seed",
    "mag",
    "trial",
    "max_gnss_error",
    "rms_residual",
    "detected",
    "detect_time"
])

# =========================================================
# Simulation loop
# =========================================================
time = np.arange(0.0, T_TOTAL + DT, DT)

for mag in SPOOF_MAGNITUDES:
    for trial in range(1, N_TRIALS + 1):

        # True vehicle state (simplified point-mass motion)
        true_x = 0.0
        true_y = 0.0

        residuals = []
        detected = 0
        detect_time = "NA"
        max_gnss_error = 0.0

        for t in time:
            # Simple low-altitude translational motion
            true_x += DT * 1.0
            true_y += DT * 0.2

            # GNSS measurement model (true position + noise)
            gnss_x = true_x + np.random.normal(0, GNSS_SIGMA)
            gnss_y = true_y + np.random.normal(0, GNSS_SIGMA)

            # Apply GNSS spoofing during attack window
            if ATTACK_START <= t <= ATTACK_END:
                gnss_x += mag

            # Navigation filter prediction (prior to GNSS update)
            # This represents the predicted state of a navigation filter
            # and is intentionally simplified (not a full inertial system)
            pred_x = true_x + np.random.normal(0, PRED_SIGMA)
            pred_y = true_y + np.random.normal(0, PRED_SIGMA)

            # Innovation / residual between GNSS measurement and prediction
            residual = np.sqrt((gnss_x - pred_x)**2 + (gnss_y - pred_y)**2)
            residuals.append(residual)

            # Detection based on residual threshold
            if not detected and residual > DETECTION_THRESHOLD:
                detected = 1
                detect_time = t

            # Track maximum GNSS position error
            gnss_error = np.sqrt((gnss_x - true_x)**2 + (gnss_y - true_y)**2)
            max_gnss_error = max(max_gnss_error, gnss_error)

            # Write time-series row
            ts_writer.writerow([
                SEED, mag, trial, round(t, 2),
                true_x, true_y,
                gnss_x, gnss_y,
                residual
            ])

        # Summary metrics
        rms_residual = np.sqrt(np.mean(np.square(residuals)))

        sum_writer.writerow([
            SEED,
            mag,
            trial,
            max_gnss_error,
            rms_residual,
            detected,
            detect_time
        ])

# =========================================================
# Close files
# =========================================================
ts_f.close()
sum_f.close()

print("Simulation complete.")
print("Time-series written to:", TS_FILE)
print("Summary written to:", SUM_FILE)
