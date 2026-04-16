import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("utility.csv")
data = df.values.flatten()

methods = ["PF", "MT", "PB", "EDF", "M-LWDF", "QUEST"]
num_methods = 6
num_users = 3
num_runs = 5

data = data.reshape(num_runs, num_methods, num_users)

# =========================
# COLORS (BY USER)
# =========================

user_colors = {
    0: "#1f77b4",  # UE1 blue
    1: "#2ca02c",  # UE2 orange
    2: "#ff7f0e"   # UE3 green
}

# =========================
# BUILD BOX DATA WITH GROUPING
# =========================

box_data = []
box_colors = []
positions = []

group_gap = 1.5
base = 1

for m in range(num_methods):

    for u in range(num_users):

        vals = data[:, m, u]

        # position inside group (slight offset per UE)
        pos = base + u * 0.25

        box_data.append(vals)
        box_colors.append(user_colors[u])
        positions.append(pos)

    base += group_gap

# =========================
# PLOT
# =========================

plt.figure(figsize=(14, 5))

bp = plt.boxplot(
    box_data,
    positions=positions,
    widths=0.2,
    showmeans=True,
    showfliers=False,
    patch_artist=True
)

# color boxes by USER
for patch, color in zip(bp["boxes"], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

for median in bp["medians"]:
    median.set_color("black")
    median.set_linewidth(1.2)

# =========================
# X AXIS = METHODS ONLY
# =========================

method_positions = [
    m * group_gap + 1 + group_gap / 2
    for m in range(num_methods)
]

plt.xticks(method_positions, methods, rotation=0)

plt.ylabel("User Satisfaction")
plt.grid(axis="y", linestyle="--", alpha=0.4)

# =========================
# LEGEND (USERS)
# =========================

legend_patches = [
    Patch(facecolor=user_colors[0], label="UE1", alpha=0.7),
    Patch(facecolor=user_colors[2], label="UE2", alpha=0.7),
    Patch(facecolor=user_colors[1], label="UE3", alpha=0.7),
]

plt.legend(handles=legend_patches, title="Users", loc="upper right")

plt.tight_layout()
plt.show()