import sys
import pandas as pd
import numpy as np
import glob

# =========================
# INPUT FILES
# =========================

if len(sys.argv) < 2:
    print("Usage: python compute_utility.py <patterns...>")
    sys.exit(1)

files = []
for pattern in sys.argv[1:]:
    files.extend(glob.glob(pattern))

if len(files) == 0:
    raise FileNotFoundError("No input files found")

# =========================
# LOSS MAP
# =========================

loss_df = pd.read_csv("loss.csv")

loss_map = {}
for _, r in loss_df.iterrows():
    key = f"{r['run']}_{r['scheduler']}_{r['ue']}"
    loss_map[key] = float(r["loss"])

# =========================
# CONFIG
# =========================

user_thresholds = {
    0: 150,
    1: 30,
    2: 60
}

# =========================
# GROUP BY RUN
# =========================

grouped = {}

for f in files:
    parts = f.replace("\\", "/").split("/")
    run = parts[1]
    grouped.setdefault(run, []).append(f)

# =========================
# OUTPUT STORAGE
# =========================

all_runs_results = []

# =========================
# MAIN LOOP
# =========================

for run in sorted(grouped.keys()):

    run_results = []

    for file in sorted(grouped[run]):

        df = pd.read_csv(file, header=None)

        # IMPORTANT: same as your original code
        df['original_user'] = df.iloc[:, 2]

        # FILTER STEP (KEEP EXACTLY)
        filtered_df = df[df.iloc[:, 9] > 0].copy()

        original_user_order = df['original_user'].unique()

        parts = file.replace("\\", "/").split("/")
        scheduler = parts[2]
        ue = parts[3].split("_")[0]

        key = f"{run}_{scheduler}_{ue}"
        loss_user = loss_map.get(key, 0.0)

        loss_idx = 0  # matches your original incremental indexing

        for user_id in original_user_order:

            group_data = filtered_df[filtered_df['original_user'] == user_id]

            if not group_data.empty:

                TBS = group_data.iloc[:, 4].tolist()
                BSR = group_data.iloc[:, 7].tolist()
                delay = group_data.iloc[:, 9].tolist()

                threshold = user_thresholds.get(user_id, 150)

                utilities = [
                    (1 - loss_user / 100)
                    * min(tbs, bsr) / bsr
                    * max(0, 1 - d / threshold) if bsr > 0 else 0
                    for tbs, bsr, d in zip(TBS, BSR, delay)
                ]

                run_results.append(np.mean(utilities) if utilities else 0)

                loss_idx += 1

    all_runs_results.append(run_results)

# =========================
# SAVE (5 × 18)
# =========================

df_out = pd.DataFrame(all_runs_results)
df_out.to_csv("utility.csv", index=False)

print("Saved utility.csv shape:", df_out.shape)