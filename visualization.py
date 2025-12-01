import matplotlib.pyplot as plt

# def plot_energy():
#     """Dummy function for initial setup."""
#     print("Graph will go here")


def plot_energy_comparison(standard_energy: float, efficient_energy: float):
    """
    Displays a professional Bar Chart comparing the total energy usage.
    """
    labels = ['Standard Scheduler', 'Energy-Efficient Scheduler']
    energy_values = [standard_energy, efficient_energy]

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#FF9999', '#66B2FF']

    bars = ax.bar(labels, energy_values, color=colors, width=0.6)

    ax.set_title('⚡ Total Energy Consumption Comparison', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Total Energy Consumed (Units)', fontsize=12)
    ax.set_xlabel('Scheduling Approach', fontsize=12)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, 
                f'{yval:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

# (You can temporarily add test calls here to ensure it works)
# if __name__ == '__main__':
#     plot_energy_comparison(550.75, 385.20)

# Optional: Test the function
# plot_energy()

import matplotlib.colors as mcolors

# --- Helper Function for Gantt Chart (Good practice) ---
def get_color(process_id):
    """
    Generates a unique, distinct color for a given process ID.
    """
    cmap = plt.get_cmap('tab10')
    return cmap(process_id % 10)

# -------------------------------------------------------------------

# This function completes the task for Commit 2

    # plt.show() # Remove this if you are integrating, keep for testing

# -------------------------------------------------------------------

# This function completes the task for Commit 3
def draw_gantt_chart(process_schedule: list):
    """
    Visualizes the CPU schedule timeline as a Gantt Chart.
    """
    if not process_schedule:
        print("No schedule data to draw the Gantt Chart.")
        return

    process_ids = sorted(list(set(p['pid'] for p in process_schedule)))
    num_processes = len(process_ids)
    pid_to_index = {pid: i for i, pid in enumerate(process_ids)}
    max_time = max(p['end'] for p in process_schedule)


    fig, ax = plt.subplots(figsize=(12, num_processes * 0.7 + 2))

    for p in process_schedule:
        pid = p['pid']
        start_time = p['start']
        duration = p['end'] - p['start']
        y_pos = pid_to_index[pid]
        color = get_color(pid)

        # Use plt.barh (horizontal bars) as required [cite: 50]
        ax.barh(y_pos, duration, left=start_time, height=0.6, 
                color=color, edgecolor='black', linewidth=0.5)
        
    ax.set_yticks(range(num_processes))
    ax.set_yticklabels([f'Process {pid}' for pid in process_ids], fontsize=10)
    ax.set_xlabel('Time (Units)', fontsize=12)
    ax.set_title('⏱️ CPU Scheduling Timeline (Gantt Chart)', fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='x', linestyle=':', alpha=0.6)

    plt.tight_layout()
    # plt.show() # Remove this if you are integrating, keep for testing