#!/usr/bin/env python3
import sys
import json
import pandas as pd
import glob
import os

if len(sys.argv) < 2:
    print("Usage: python extract_loss.py users_3/run_*/scheduler_*/UE*_irtt_report.json")
    sys.exit(1)

rows = []

for pattern in sys.argv[1:]:
    for file in glob.glob(pattern):

        with open(file) as f:
            data = json.load(f)

        loss = data.get("stats", {}).get("upstream_loss_percent", None)
        if loss is None:
            continue

        parts = file.replace("\\", "/").split("/")

        run = parts[1]
        scheduler = parts[2]
        ue = parts[3].split("_")[0]

        rows.append({
            "run": run,
            "scheduler": scheduler,
            "ue": ue,
            "loss": loss
        })

df = pd.DataFrame(rows)

# append (IMPORTANT)
out_file = "loss.csv"
if os.path.exists(out_file):
    df.to_csv(out_file, mode="a", index=False, header=False)
else:
    df.to_csv(out_file, index=False)

print(df)
print("Appended to loss.csv")