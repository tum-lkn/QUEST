# Time Synchronization (PTP)

## Overview

Accurate time synchronization between all devices (UEs, gNB, and core network PCs) is essential to ensure **correct delay measurements**.
Without proper synchronization, measured delays may be inconsistent or even negative.

In this project, we use the **Precision Time Protocol (PTP)** for high-accuracy synchronization.

---

## Precision Time Protocol (PTP)

PTP provides sub-microsecond synchronization accuracy and is therefore preferred over other methods for experimental evaluation.

We use the Linux implementation **`linuxptp`**, which includes the tools:

* `ptp4l` – synchronizes clocks across the network
* `phc2sys` – synchronizes system time with the hardware clock (if available)

---

## Installation

Install the required package on all devices:

```bash
sudo apt update
sudo apt install linuxptp
```

---

## Hardware & Driver Support

For best performance, your network interface card (NIC) and driver should support **hardware timestamping**.

Check support using:

```bash
ethtool -T <interface>
```

Example:

```bash
ethtool -T eth0
```

---

## Synchronization Setup

### 1. Master Clock

On the selected master node:

```bash
# Start PTP daemon
sudo ptp4l -i <interface> -m -A -4

# Synchronize system clock with hardware clock
sudo phc2sys -c CLOCK_REALTIME -s <interface> -O 0 -w -m
```

---

### 2. Client Nodes (UEs, gNB, Core)

On all other nodes:

```bash
# Start PTP daemon
sudo ptp4l -i <interface> -m -A -4

# Synchronize system clock
sudo phc2sys -c CLOCK_REALTIME -s <interface> -O 0 -w -m
```

---

## Notes

* Replace `<interface>` with your network interface (e.g., `eth0`)
* UDP mode (`-4`) is used for transport over IP networks
* For best accuracy, ensure all intermediate network devices support PTP
* If hardware timestamping is not available, PTP will fall back to software mode with reduced accuracy

---

## Reference

* https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/deployment_guide/ch-configuring_ptp_using_ptp4l
