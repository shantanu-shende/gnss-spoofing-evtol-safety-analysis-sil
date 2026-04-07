# Evaluating GNSS Spoofing as a Cyber-Safety Risk in eVTOL Aircraft

### Pilot Software-in-the-Loop (SIL) Study
**Technische Hochschule Mittelhessen · Cybersecurity Research · 2025-26**  
**Author:** Shantanu Shende

---

## Overview

This repository contains a **pilot research study** investigating whether **GNSS spoofing**
poses a **credible cyber-safety risk** to **electric Vertical Take-Off and Landing (eVTOL) aircraft**
during **low-altitude operations**, specifically **take-off and landing**.

The project follows a **software-in-the-loop (SIL)** methodology and is designed as an
early-stage, **reproducible** and **independently verifiable** analysis suitable for
academic evaluation and future safety-oriented extensions.

The repository includes:

- A fully open **Python-based SIL simulation**
- A **residual-based navigation consistency monitor**
- Controlled **GNSS spoofing scenarios**
- Automatically generated **figures and metrics**
- A complete **LaTeX research paper** prepared for submission

---

## Research Motivation

Future **Urban Air Mobility (UAM)** concepts rely heavily on **Global Navigation Satellite Systems (GNSS)**
for positioning, even during safety-critical low-altitude phases where margins for error are limited.

GNSS spoofing—where counterfeit satellite-like signals are transmitted to mislead a receiver—
represents a **plausible external cyber-physical threat** that does **not require internal system access**.

This study investigates the following research question:

> **Can GNSS spoofing introduce navigation deviations that become safety-relevant for eVTOL aircraft during low-altitude operations?**

The work is intended as a **risk-oriented exploratory analysis**, not as a certification-level navigation system evaluation.

---

## Summary of Experiment

A lightweight **Python-based SIL simulator** models:

- A simplified low-altitude eVTOL trajectory
- GNSS and IMU-like sensor behavior
- Controlled spoofing offsets of **0 m, 10 m, 30 m, and 60 m**
- A defined attack window (**10–30 seconds**)
- Multiple trials per spoofing magnitude
- A simplified **residual-based consistency detector**

### Outputs Generated

- True vs GNSS-reported trajectories
- Residual magnitude time-series
- Maximum GNSS error distributions
- Detection timing and rates

All results are generated using **open-source tools only** and are reproducible using a fixed random seed.

The resulting figures are incorporated directly into the accompanying LaTeX paper.

---

## How to Reproduce (Windows 10/11)

### 1. Clone the repository
```Open powershell```
git clone https://github.com/sssh02.git
cd sssh02

### 2. Create & activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the simulation
python experiments/sim/simple_evtol_sim.py

### 5. Generate plots
python experiments/sim/plot_results.py

### 6. Figures appear in:
experiments/sim/
paper/figures/

### 7. Build the LaTeX paper
Using IntelliJ, VS Code, or Overleaf:
paper/main.tex → Compile → main.pdf ...
=======
# gnss-spoofing-evtol-safety-analysis-sil
Software-in-the-loop (SIL) simulation for evaluating GNSS spoofing as a cyber-safety risk for eVTOL aircraft during low-altitude operations. Includes GNSS/IMU navigation modeling, spoofing injection, and residual-based detection analysis.
>>>>>>> 62c385f54df239282959ef8dc2a9faea2ea7702b
