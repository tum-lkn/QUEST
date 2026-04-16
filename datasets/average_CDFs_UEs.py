import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.interpolate import interp1d
import tikzplotlib

# =========================
# CONFIGURATION
# =========================

num_methods = 6
num_users = 3

labels = ["PF", "MT", "PB", "EDF", "M-LWDF", "QUEST"]

# Delay thresholds per user (ms)
user_thresholds = {
    '0': 150,   # User 2 (5QI=2)
    '1': 30,   # User 1 (5QI=84)
    '2': 60   # User 3 (5QI=69)
}

OUTPUT_DIR = "results"
save_figures = False

# CSV structure assumptions
USER_COL = 2
DELAY_COL = 9

# =========================
# CHECK INPUT
# =========================

if len(sys.argv) < 2:
    print("Usage: python3 your_script.py file1_method1.csv file1_method2.csv ... file2_method1.csv ...")
    sys.exit(1)

# Command-line arguments for file paths
file_paths = sys.argv[1:]  # Files passed as arguments
num_runs = len(file_paths) // num_methods  # Calculate the number of runs based on inputs

# Check if the number of files matches the expected format
if len(file_paths) % num_methods != 0:
    print("Error: The number of files must be a multiple of the number of methods.")
    sys.exit(1)

all_runs_data = {run_idx: {method_idx: {user_idx: [] for user_idx in range(num_users)} for method_idx in range(num_methods)} for run_idx in range(num_runs)}

# Load data
for idx, file_path in enumerate(file_paths):
    run_idx = idx // num_methods  # Determine the run index
    method_idx = idx % num_methods  # Determine the method index
    try:
        df = pd.read_csv(file_path, header=None)
        # Filter rows where column index 9 is greater than 0 (delays > 0)
        filtered_df = df[df.iloc[:, DELAY_COL] > 0].copy()
        filtered_df['original_user'] = filtered_df.iloc[:, USER_COL]  # Assuming user IDs are in the 3rd column

        # Preserve the original order of user IDs
        original_user_order = filtered_df['original_user'].unique()

        # Process each user
        user_id=-1
        for user_idx in original_user_order:
            user_id=user_id+1
            group_data = filtered_df[filtered_df['original_user'] == user_idx]

            if not group_data.empty:
                delay = group_data.iloc[:, DELAY_COL].tolist()
                all_runs_data[run_idx][method_idx][user_id].extend(delay)
    except FileNotFoundError:
        print(f"File {file_path} not found. Skipping.")

# Debugging: Print loaded data for checking
print("All runs data loaded:")
for run_idx in range(num_runs):
    print(f"Run {run_idx + 1}:")
    for method_idx in range(num_methods):
        print(f"Method {labels[method_idx]}:")
        for user_idx in range(num_users):
            print(f"User {user_idx}: {len(all_runs_data[run_idx][method_idx][user_idx])} delays")
            
# Compute dropped packet fractions for every run
dropped_packets_per_run = {
    run_idx: {method_idx: {user_idx: 0.0 for user_idx in range(num_users)}
              for method_idx in range(num_methods)}
    for run_idx in range(num_runs)
}

for run_idx in range(num_runs):
    for method_idx in range(num_methods):
        for user_idx in range(num_users):
            delays = np.array(all_runs_data[run_idx][method_idx][user_idx])
            if len(delays) > 0:
                ecdf = ECDF(delays)
                threshold = user_thresholds[str(user_idx)]
                dropped_packets_per_run[run_idx][method_idx][user_idx] = 1 - ecdf(threshold)
            else:
                dropped_packets_per_run[run_idx][method_idx][user_idx] = 0.0

# Print per-run dropped fractions
for run_idx in range(num_runs):
    print(f"\nRun {run_idx + 1}:")
    for method_idx in range(num_methods):
        fractions = dropped_packets_per_run[run_idx][method_idx]
        print(f"Method {labels[method_idx]}: {fractions}")

# Plot ECDF for each run and user
for run_idx in range(num_runs):
    fig, axes = plt.subplots(1, num_users, figsize=(18, 5), sharey=True)
    for user_idx in range(num_users):  # 3 users
        ax = axes[user_idx]
        ax.set_title(f"Run {run_idx + 1}, User {user_idx + 1} ECDF")
        for method_idx in range(num_methods):
            sns.kdeplot(all_runs_data[run_idx][method_idx][user_idx], ax=ax, label=labels[method_idx], linewidth=2, cumulative=True, bw_adjust=1)
        delay_threshold = user_thresholds[str(user_idx)]
        ax.axvline(x=delay_threshold, color='red', linestyle='--', label=f'Threshold ({delay_threshold} ms)')
        ax.set_xlim(0, delay_threshold)
        ax.set_xlabel("Delay (ms)")
        ax.set_ylabel("Cumulative Probability")
        ax.legend(loc="best")
        ax.grid(True)
    plt.tight_layout()
    plt.show()

# Aggregate data across runs for each user and method
aggregated_data = {method_idx: {user_idx: [] for user_idx in range(num_users)} for method_idx in range(num_methods)}

for run_idx in range(num_runs):
    for method_idx in range(num_methods):
        for user_idx in range(num_users):
            aggregated_data[method_idx][user_idx].extend(all_runs_data[run_idx][method_idx][user_idx])

# Debugging: Print aggregated data for checking
print("\nAggregated data across runs:")
for method_idx in range(num_methods):
    print(f"Method {labels[method_idx]}:")
    for user_idx in range(num_users):
        print(f"  User {user_idx}: {len(aggregated_data[method_idx][user_idx])} delays")

# Plot aggregated ECDFs for all users
fig, axes = plt.subplots(1, num_users, figsize=(18, 5), sharey=True)
for user_idx in range(num_users):  # Users
    ax = axes[user_idx]
    ax.set_title(f"Aggregated ECDF for User {user_idx + 1}")
    for method_idx in range(num_methods):
        sns.kdeplot(
            aggregated_data[method_idx][user_idx], 
            ax=ax, label=labels[method_idx], linewidth=2, cumulative=True, bw_adjust=1
        )
    delay_threshold = user_thresholds[str(user_idx)]
    ax.axvline(x=delay_threshold, color='red', linestyle='-', label=f'Threshold ({delay_threshold} ms)')
    ax.set_xlim(0, delay_threshold)
    ax.set_xlabel("Delay (ms)")
    ax.set_ylabel("Aggregated CDF")
    ax.legend()  # Ensure a legend is created
    ax.grid(True)
plt.tight_layout()
# tikzplotlib.save("UE_measurements_CDF.tex")
plt.show()


# Mean and Variance of ECDFs
delay_points = np.linspace(0, 150, 100)  # Common delay points
interpolated_cdfs = {method_idx: {user_idx: [] for user_idx in range(num_users)} for method_idx in range(num_methods)}

for run_idx in range(num_runs):
    for method_idx in range(num_methods):
        for user_idx in range(num_users):
            ecdf = ECDF(all_runs_data[run_idx][method_idx][user_idx])
            interp_cdf = interp1d(ecdf.x, ecdf.y, bounds_error=False, fill_value=(0, 1))
            interpolated_cdfs[method_idx][user_idx].append(interp_cdf(delay_points))

mean_cdfs = {
    method_idx: {user_idx: np.mean(interpolated_cdfs[method_idx][user_idx], axis=0) for user_idx in range(num_users)}
    for method_idx in range(num_methods)
}
std_cdfs = {
    method_idx: {user_idx: np.std(interpolated_cdfs[method_idx][user_idx], axis=0) for user_idx in range(num_users)}
    for method_idx in range(num_methods)
}

# Plot Mean CDFs with Variability
fig, axes = plt.subplots(1, num_users, figsize=(18, 5), sharey=True)
for user_idx in range(num_users):  # Users
    ax = axes[user_idx]
    ax.set_title(f"Mean ECDF with Variability for User {user_idx + 1}")
    for method_idx in range(num_methods):
        mean_cdf = mean_cdfs[method_idx][user_idx]
        std_cdf = std_cdfs[method_idx][user_idx]
        ax.plot(delay_points, mean_cdf, label=labels[method_idx])
        ax.fill_between(
            delay_points,
            mean_cdf - std_cdf,
            mean_cdf + std_cdf,
            alpha=0.2
        )
    delay_threshold = user_thresholds[str(user_idx)]
    ax.axvline(x=delay_threshold, color='red', linestyle='--', label=f'Threshold ({delay_threshold} ms)')
    ax.set_xlim(0, delay_threshold)
    ax.set_xlabel("Delay (ms)")
    ax.set_ylabel("Cumulative Probability")
    ax.legend(loc="best")
    ax.grid(True)
plt.tight_layout()
plt.show()