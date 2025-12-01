import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# --- Helper Function for Gantt Chart (Optional but good practice) ---
def get_color(process_id):
    """
    Generates a unique, distinct color for a given process ID.
    Using a standard colormap for professional appearance.
    """
    # Use 'tab10' colormap, which is designed for categorical data
    cmap = plt.get_cmap('tab10')
    return cmap(process_id % 10)

# -------------------------------------------------------------------

def plot_energy_comparison(standard_energy: float, efficient_energy: float):
    """
    Displays a professional Bar Chart comparing the total energy usage
    of a standard and an energy-efficient scheduling approach.

    Args:
        standard_energy: Total energy consumed by the standard scheduler.
        efficient_energy: Total energy consumed by the efficient scheduler.
    """
    labels = ['Standard Scheduler', 'Energy-Efficient Scheduler']
    energy_values = [standard_energy, efficient_energy]

    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(8, 6))

    # Define colors for the bars
    colors = ['#FF9999', '#66B2FF'] # Light Red and Light Blue

    # Create the bar chart
    bars = ax.bar(labels, energy_values, color=colors, width=0.6)

    # Add titles and labels for professionalism
    ax.set_title('⚡ Total Energy Consumption Comparison', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Total Energy Consumed (Units)', fontsize=12)
    ax.set_xlabel('Scheduling Approach', fontsize=12)

    # Add energy values on top of the bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, 
                f'{yval:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Customize the appearance for a report
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.7) # Add grid lines for readability

    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------

def draw_gantt_chart(process_schedule: list):
    """
    Visualizes the CPU schedule timeline as a Gantt Chart.

    Args:
        process_schedule: A list of dictionaries, where each dict represents
                          a completed process slice:
                          [
                              {'pid': 1, 'start': 0, 'end': 5, 'ct': 10},
                              {'pid': 2, 'start': 5, 'end': 15, 'ct': 15},
                              ...
                          ]
                          'pid' is the Process ID, 'start' and 'end' are the times.
                          'ct' (Completion Time) is used to label the process.
    """
    if not process_schedule:
        print("No schedule data to draw the Gantt Chart.")
        return

    # 1. Prepare Data for Plotting
    process_ids = sorted(list(set(p['pid'] for p in process_schedule)))
    num_processes = len(process_ids)
    
    # Map Process ID to its index for Y-axis plotting
    pid_to_index = {pid: i for i, pid in enumerate(process_ids)}
    
    # Determine the maximum time for the X-axis limit
    max_time = max(p['end'] for p in process_schedule)
    
    # Find the completion time for the label
    completion_times = {p['pid']: p['ct'] for p in process_schedule}


    # 2. Create the Figure and Axes
    fig, ax = plt.subplots(figsize=(12, num_processes * 0.7 + 2))

    # 3. Plot the Schedule Slices
    for p in process_schedule:
        pid = p['pid']
        start_time = p['start']
        duration = p['end'] - p['start']
        y_pos = pid_to_index[pid]
        
        color = get_color(pid)

        # Plot the bar for the slice: (x_start, y_center, duration, height)
        ax.barh(y_pos, duration, left=start_time, height=0.6, 
                color=color, edgecolor='black', linewidth=0.5, label=f'P{pid}')
        
        # Add the Process ID label inside the bar (if duration is long enough)
        if duration > max_time * 0.03: # Heuristic check for space
            ax.text(start_time + duration / 2, y_pos, f'P{pid}', 
                    ha='center', va='center', color='white', fontsize=8, fontweight='bold')


    # 4. Customize the Appearance
    # Set Y-axis ticks and labels (Process IDs)
    ax.set_yticks(range(num_processes))
    ax.set_yticklabels([f'Process {pid}' for pid in process_ids], fontsize=10)
    ax.set_ylim(-0.8, num_processes - 0.2) # Adjust limits for better spacing

    # Set X-axis label and title
    ax.set_xlabel('Time (Units)', fontsize=12)
    ax.set_title('⏱️ CPU Scheduling Timeline (Gantt Chart)', fontsize=16, fontweight='bold', pad=20)
    
    # Show grid lines for time reference
    ax.grid(axis='x', linestyle=':', alpha=0.6)
    
    # Add Completion Time annotations (optional, but informative)
    for pid, ct in completion_times.items():
        y_pos = pid_to_index[pid]
        # Place a vertical line and a text marker at the completion time
        ax.axvline(x=ct, ymin=(y_pos + 0.1)/num_processes, ymax=(y_pos + 0.9)/num_processes, 
                   color=get_color(pid), linestyle='--', linewidth=1)
        ax.text(ct + 0.2, y_pos + 0.3, f'CT={ct}', fontsize=8, color='black', ha='left', va='center')


    plt.tight_layout()
    plt.show()

# -------------------- Example Usage (for testing) --------------------

if __name__ == '__main__':
    print("--- 1. Testing plot_energy_comparison ---")
    
    # Sample data
    standard_energy_data = 550.75
    efficient_energy_data = 385.20
    
    plot_energy_comparison(standard_energy_data, efficient_energy_data)
    

    print("\n--- 2. Testing draw_gantt_chart ---")
    
    # Sample schedule data: 3 processes, with preemptions for P1
    sample_schedule = [
        {'pid': 1, 'start': 0, 'end': 3, 'ct': 15}, # P1 runs
        {'pid': 2, 'start': 3, 'end': 8, 'ct': 15}, # P2 runs
        {'pid': 3, 'start': 8, 'end': 10, 'ct': 15},# P3 runs
        {'pid': 1, 'start': 10, 'end': 15, 'ct': 15} # P1 finishes
    ]

    draw_gantt_chart(sample_schedule)