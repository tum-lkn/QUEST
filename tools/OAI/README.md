#  QUEST-Enhanced OpenAirInterface (OAI) 

## Overview

This repository contains modifications to the **OpenAirInterface (OAI)** 5G NR stack to support the **QUEST** operation.

These enhancements extend both transmitter-side (UE) and receiver-side (gNB) implementations to enable reproducible evaluation of multiple scheduling strategies in a realistic 5G NR environment.

Original OAI: https://gitlab.eurecom.fr/oai/openairinterface5g

---

## Software Versions

This work is based on the following OAI components:

- **UE (RAN side):** OpenAirInterface tag `2024.w09`
- **gNB (RAN side):** OpenAirInterface tag `2024.w09`
- **Core Network (CN):** OpenAirInterface tag `2024.w04`

All modifications are applied on top of these stable tagged releases to ensure reproducibility. 

We provide patches the include modifications for each component, as well as the config files used for gNB and CN.

In scripts folder find the respective scripts for executing each component. 

## 📶 UE (Transmitter-Side) Enhancements

The UE implementation is extended to:

1. Include **HOL delay information in Buffer Status Reports (BSR)**
2. Enable per-SDU timing tracking at the RLC layer
3. Support estimation of uplink queuing delay before transmission

These modifications allow delay-awareness to be propagated from RLC to MAC and used in uplink scheduling decisions.

---

## 📡 gNB (Receiver-Side) Enhancements

The gNB implementation is extended to:

### 1. HOL Delay Extraction
- Extract HOL delay information reported by UEs
- Parse delay-related fields inside MAC UL procedures

### 2. QoS Flow Retrieval
- Retrieve QoS flow parameters from configured DRBs in MAC
- Map **5QI / QFI values** to active QoS flows
- Use QoS parameters for scheduling decisions

### 3. UL Transmission Delay Measurement
- Capture uplink packet reception timestamps
- Compute uplink transmission delay per packet

### 4. Scheduling Algorithms
The following uplink schedulers are implemented and evaluated in addition to default **PF** (Proportional Fair) scheduler:

- **MT** (Maximum Throughput)
- **PB** (Priority-Based)
- **EDF** (Earliest Deadline First)
- **M-LWDF** (Modified Largest Weighted Delay First)
- **QUEST** (proposed scheduler)

---

## 📊 Experimental Methodology

Each scheduling scheme is evaluated under identical conditions:

- Each experiment consists of **5 independent runs**
- Each run lasts **30 seconds**
- Between runs, UE positions are changed relative to the gNB
  - Ensures diverse channel conditions across runs
- During each run:
  - All devices remain static
  - Channel conditions remain stable for fair comparison

---
