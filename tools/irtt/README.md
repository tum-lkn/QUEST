# Isochronous Round Trip Tester (IRTT) – Modified for QUEST

## Overview

This repository contains a modified version of the **Isochronous Round Trip Tester (IRTT)** used within the QUEST framework for low-latency network experiments and scheduler evaluation.

IRTT is used to generate controlled traffic flows and measure end-to-end latency in OAI-based systems.

Original tool:
https://github.com/heistp/irtt

---

## Purpose of This Modified Version

The original IRTT tool has been extended to support **research-grade delay measurements** required by QUEST.

The modifications enable:

- Precise packet timestamping at the UE (client side)
- Timestamp extraction at the server (gNB/core side)
- Computation of uplink packet delay
- Structured logging for offline analysis
- Optional real-time export to external schedulers

## System Requirements

- Utilized Go 1.22.0
- Linux (Ubuntu recommended)
- PTP synchronization (linuxptp)

Optional tools:
- ssh / scp
- bash utilities

---

## ⚠ Critical Requirement: Time Synchronization

All nodes MUST be synchronized using PTP.

Without synchronization:
- delays are incorrect
- negative values may appear
- results are invalid

---

## 🔧 Build Workflow (Modified IRTT)

This version is NOT installed via `go install ...@latest`.
Instead clone the irtt repository in https://github.com/heistp/irtt and apply the provided patches:
- 0001-client-modifications.patch at IRTT client side (UEs)
- 0002-server-modifications.patch at IRTT server side (CN or gNB)

Apply `go install -buildvcs=false ./...` to build the **locally modified repository**.
If the build completes successfully, no output is printed.

If dependency or module-related errors appera, explicitly enable Go modules: `export GO111MODULE=on`. Then rebuild again.

Some QUEST extensions require additional Go packages (e.g., SSH/SCP integration)
- `sudo /usr/local/go/bin/go get github.com/bramvdbogaerde/go-scp`
- `sudo /usr/local/go/bin/go get golang.org/x/crypto/ssh`

Ensure the correct version is used `cp $HOME/go/bin/irtt /usr/local/go/bin/irtt`.

## Usage

### Server (gNB / Core Network)

```bash
  irtt server -b <SERVER_IP>:<PORT> --tstamp=dual -o delay_data_CN.txt -r delay_data_gNB.txt
```

---

### Client (UE)
```bash
irtt client -i 20ms -d 0.5m -l 1000 --fill=rand --sfill=rand <SERVER_IP>:<PORT> --clock=both -o ${scheduler}_UE1_irtt_report.json
```
---

---

## 📁 Repository Structure

Modified files include:

- `client.go` → UE timestamping
- `irtt_server.go` → server logging + SSH/SCP
- `conn.go` → packet capture modifications
- `sconn.go` → HOL computation + file writing
- `defaults.go`, `sconfig.go` → CLI extensions
- `output.json` → runtime logs

---