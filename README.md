# QUEST

**A. Jano, S. Ayvaşik, Y. Deshpande and W. Kellerer, "QUEST: User-Based Quality of Service Aware Uplink Resource Scheduling", accepted in IEEE Transactions on Network and Service Management.**

A closely related version is available as a TechRxiv preprint for reference:
https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.176110126.66841255/v1

QUEST is a QoS-aware UL scheduling framework that exploits the 5G QoS model alongside network and device context to efficiently allocate radio resources.

---

## Repository Structure

- `dataset/` – Experiment datasets used in the paper (2 and 3 UE scenarios)
- `docs/` – Documentation for setup, configuration, and synchronization
- `scripts/` – Automation scripts to deploy components and process results
- `tools/` – Patches and helper tools required to modify external dependencies

---

## System Requirements

QUEST builds on the following external components:

### OpenAirInterface (OAI)
- UE, gNB, and Core Network (CN)
- Installation guide: https://gitlab.eurecom.fr/oai/openairinterface5g
- Required versions are specified in: `tools/OAI/README.md`

### IRTT (Interactive RTT Tool)
- Repository: https://github.com/heistp/irtt
- Modified version is required (see `tools/irtt/README.md`)

### PTP Synchronization
- Used for time synchronization between nodes
- Setup instructions: `docs/synchronization.md`

---

## Installation and Setup

### 1. Install OAI Components

Install OpenAirInterface UE, gNB, and CN following the official documentation.

After installation:

- Apply QUEST patches located in `tools/OAI/`
- Ensure all modifications are correctly applied before compilation
- Modify the uplink scheduler in: openair2/LAYER2/NR_MAC_gNB/gNB_scheduler_ulsch.c


> ⚠ Only one scheduler configuration flag should be enabled at a time.

Rebuild UE/gNB after applying changes.

---

### 2. Install and Patch IRTT

Install IRTT following the official documentation:

https://github.com/heistp/irtt

Then apply QUEST modifications:

- Apply patches in `tools/irtt/`

Configuration:
- IRTT **client runs on the UE**
- IRTT **server runs on the CN**
- For multi-UE experiments, use different server ports per UE

---

### 3. Time Synchronization (PTP)

Configure Precision Time Protocol (PTP) synchronization between nodes:

- See: `docs/synchronization.md`

Accurate synchronization is required for valid delay measurements.

---

### 4. Running Experiments

Use the scripts provided in the `scripts/` directory to start:

- Core Network
- gNB
- UE instances
- IRTT server and clients

Ensure all file paths are correctly configured for your environment.

---

## Data Collection

Each experiment produces:

- `.csv` files containing scheduler-level performance metrics
- `.json` files on each UE containing IRTT delay reports

---

## Data Processing

The framework provides utilities to extract and process delay measurements:

- `irtt_json_to_csv.sh` – Convert a single `.json` file into `.csv`
- `batch_convert.sh` – Batch conversion for multiple `.json` files

---

## Notes

- All OAI patches must be applied before building components
- Only one scheduler mode should be active at any time
- PTP synchronization is mandatory for correct latency evaluation

## Evaluation
The gNB_results.csv file include the following info: FRAME, SLOT, UE_RNTI, SINR, TBS, MCS NR_PRBS, HOL_DELAY, UL_DELAY


---

#### 1. Delay Analysis 

```bash
python average_CDFs_UEs.py users_3/run_1/scheduler_PF/gNB_results.csv users_3/run_1/scheduler_MT/gNB_results.csv users_3/run_1/scheduler_PB/gNB_results.csv users_3/run_1/scheduler_EDF/gNB_results.csv users_3/run_1/scheduler_M-LWDF/gNB_results.csv users_3/run_1/scheduler_QUEST/gNB_results.csv users_3/run_2/scheduler_PF/gNB_results.csv users_3/run_2/scheduler_MT/gNB_results.csv users_3/run_2/scheduler_PB/gNB_results.csv users_3/run_2/scheduler_EDF/gNB_results.csv users_3/run_2/scheduler_M-LWDF/gNB_results.csv users_3/run_2/scheduler_QUEST/gNB_results.csv users_3/run_3/scheduler_PF/gNB_results.csv users_3/run_3/scheduler_MT/gNB_results.csv users_3/run_3/scheduler_PB/gNB_results.csv users_3/run_3/scheduler_EDF/gNB_results.csv users_3/run_3/scheduler_M-LWDF/gNB_results.csv users_3/run_3/scheduler_QUEST/gNB_results.csv users_3/run_4/scheduler_PF/gNB_results.csv users_3/run_4/scheduler_MT/gNB_results.csv users_3/run_4/scheduler_PB/gNB_results.csv users_3/run_4/scheduler_EDF/gNB_results.csv users_3/run_4/scheduler_M-LWDF/gNB_results.csv users_3/run_4/scheduler_QUEST/gNB_results.csv users_3/run_5/scheduler_PF/gNB_results.csv users_3/run_5/scheduler_MT/gNB_results.csv users_3/run_5/scheduler_PB/gNB_results.csv users_3/run_5/scheduler_EDF/gNB_results.csv users_3/run_5/scheduler_M-LWDF/gNB_results.csv users_3/run_5/scheduler_QUEST/gNB_results.csv
```
#### 2. User Satisfaction analysis
Collect the UL packet loss for each run:
```bash
python extract_loss.py users_3/run_1/scheduler_PF/UE*_irtt_report.json users_3/run_1/scheduler_MT/UE*_irtt_report.json users_3/run_1/scheduler_PB/UE*_irtt_report.json users_3/run_1/scheduler_EDF/UE*_irtt_report.json users_3/run_1/scheduler_M-LWDF/UE*_irtt_report.json users_3/run_1/scheduler_QUEST/UE*_irtt_report.json
```
Compute user satisfaction:
```bash
python compute_utility.py users_3/run_1/scheduler_PF/gNB_results.csv users_3/run_1/scheduler_MT/gNB_results.csv users_3/run_1/scheduler_PB/gNB_results.csv users_3/run_1/scheduler_EDF/gNB_results.csv users_3/run_1/scheduler_M-LWDF/gNB_results.csv users_3/run_1/scheduler_QUEST/gNB_results.csv users_3/run_2/scheduler_PF/gNB_results.csv users_3/run_2/scheduler_MT/gNB_results.csv users_3/run_2/scheduler_PB/gNB_results.csv users_3/run_2/scheduler_EDF/gNB_results.csv users_3/run_2/scheduler_M-LWDF/gNB_results.csv users_3/run_2/scheduler_QUEST/gNB_results.csv users_3/run_3/scheduler_PF/gNB_results.csv users_3/run_3/scheduler_MT/gNB_results.csv users_3/run_3/scheduler_PB/gNB_results.csv users_3/run_3/scheduler_EDF/gNB_results.csv users_3/run_3/scheduler_M-LWDF/gNB_results.csv users_3/run_3/scheduler_QUEST/gNB_results.csv users_3/run_4/scheduler_PF/gNB_results.csv users_3/run_4/scheduler_MT/gNB_results.csv users_3/run_4/scheduler_PB/gNB_results.csv users_3/run_4/scheduler_EDF/gNB_results.csv users_3/run_4/scheduler_M-LWDF/gNB_results.csv users_3/run_4/scheduler_QUEST/gNB_results.csv users_3/run_5/scheduler_PF/gNB_results.csv users_3/run_5/scheduler_MT/gNB_results.csv users_3/run_5/scheduler_PB/gNB_results.csv users_3/run_5/scheduler_EDF/gNB_results.csv users_3/run_5/scheduler_M-LWDF/gNB_results.csv users_3/run_5/scheduler_QUEST/gNB_results.csv
```
Final plot:
```bash
python plot_utility.py
```