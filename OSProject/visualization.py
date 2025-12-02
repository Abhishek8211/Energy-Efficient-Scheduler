import matplotlib.pyplot as plt
import numpy as np

# def plot_energy():
#     """Dummy function for initial setup."""
#     print("Graph will go here")


def plot_energy_comparison(standard_energy: float, efficient_energy: float):
    """
    Modern, professional energy comparison chart with gradient bars,
    shadows, and enhanced visual appeal.
    """
    labels = ['Standard\nScheduler', 'Energy-Efficient\nScheduler']
    energy_values = [standard_energy, efficient_energy]

    # Modern color palette with gradients
    colors = ['#ef4444', '#06b6d4']  # Red and Cyan
    edge_colors = ['#dc2626', '#0891b2']
    
    # Create figure with dark background
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    # Create bars with enhanced styling
    bars = ax.bar(labels, energy_values, color=colors, width=0.5, 
                   edgecolor=edge_colors, linewidth=3, alpha=0.9)
    
    # Add gradient effect using patches
    for i, bar in enumerate(bars):
        # Add shadow effect
        shadow = plt.Rectangle((bar.get_x() - 0.01, 0), 
                               bar.get_width(), bar.get_height(),
                               facecolor='black', alpha=0.2, zorder=0)
        ax.add_patch(shadow)
        
        # Add inner glow
        glow_height = bar.get_height() * 0.95
        glow = plt.Rectangle((bar.get_x() + 0.02, bar.get_height() * 0.05), 
                             bar.get_width() - 0.04, glow_height,
                             facecolor='white', alpha=0.1, zorder=2)
        ax.add_patch(glow)

    # Enhanced title with custom styling
    ax.set_title('⚡ Total Energy Consumption Comparison', 
                 fontsize=26, fontweight='bold', pad=30,
                 color='#e0f2fe', family='sans-serif')
    
    ax.set_ylabel('Total Energy Consumed (mW)', 
                  fontsize=16, fontweight='bold', color='#94a3b8', labelpad=15)
    ax.set_xlabel('Scheduling Approach', 
                  fontsize=16, fontweight='bold', color='#94a3b8', labelpad=15)

    # Enhanced value labels on top of bars
    for i, bar in enumerate(bars):
        yval = bar.get_height()
        # Value with background
        bbox_props = dict(boxstyle='round,pad=0.5', facecolor=colors[i], 
                         edgecolor='white', linewidth=2, alpha=0.9)
        ax.text(bar.get_x() + bar.get_width()/2, yval + max(energy_values) * 0.03, 
                f'{yval:.2f} mW', 
                ha='center', va='bottom', 
                fontsize=14, fontweight='bold', 
                color='white', bbox=bbox_props)

    # Calculate and display savings with enhanced styling
    savings = ((standard_energy - efficient_energy) / standard_energy * 100) if standard_energy > 0 else 0
    
    # Savings badge
    badge_y = max(energy_values) * 0.5
    badge_props = dict(boxstyle='round,pad=0.8', facecolor='#10b981', 
                      edgecolor='#059669', linewidth=3, alpha=0.95)
    ax.text(0.5, badge_y, 
            f'💰 Energy Savings: {savings:.1f}%', 
            ha='center', va='center',
            fontsize=18, fontweight='bold', 
            color='white', bbox=badge_props,
            transform=ax.transData, zorder=10)

    # Modern grid
    ax.grid(axis='y', linestyle='--', alpha=0.2, color='#475569', linewidth=1)
    ax.set_axisbelow(True)
    
    # Clean spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#475569')
        ax.spines[spine].set_linewidth(2)
    
    # Style tick labels
    ax.tick_params(colors='#94a3b8', labelsize=12, width=2, length=6)
    for label in ax.get_xticklabels():
        label.set_fontweight('bold')
        label.set_color('#e0f2fe')
        label.set_fontsize(14)
    
    # Add subtle animation-like effect with arrows
    if savings > 0:
        arrow_props = dict(arrowstyle='->', lw=3, color='#10b981', 
                          connectionstyle='arc3,rad=.3')
        ax.annotate('', xy=(1, efficient_energy), xytext=(0, standard_energy),
                   arrowprops=arrow_props, zorder=5)

    plt.tight_layout(pad=2)
    plt.savefig('energy_comparison.png', dpi=300, bbox_inches='tight', 
                facecolor='#0f172a')
    print("✅ Saved: energy_comparison.png")
    
    fig.canvas.manager.set_window_title('⚡ Energy Consumption Analysis')
    plt.show(block=True)


# --- Helper Function for Gantt Chart (Good practice) ---
def get_color(process_id):
    """
    Generates a unique, distinct color for a given process ID.
    """
    cmap = plt.get_cmap('tab10')
    return cmap(abs(process_id) % 10)  # Use abs() to handle negative hash values

# -------------------------------------------------------------------

def draw_gantt_chart(process_schedule: list):
    """
    Modern, professional Gantt chart with gradient bars, shadows,
    enhanced labels, and clean design.
    """
    if not process_schedule:
        print("No schedule data to draw the Gantt Chart.")
        return

    process_ids = sorted(list(set(p['pid'] for p in process_schedule)))
    num_processes = len(process_ids)
    pid_to_index = {pid: i for i, pid in enumerate(process_ids)}
    max_time = max(p['end'] for p in process_schedule)

    # Dynamic figure size
    fig_width = max(16, max_time / 40)
    fig_height = max(9, num_processes * 1.5 + 3)
    
    # Dark themed figure
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    
    # Modern color palette for different processes
    modern_colors = ['#3b82f6', '#06b6d4', '#8b5cf6', '#ec4899', 
                     '#f59e0b', '#10b981', '#ef4444', '#6366f1']

    for p in process_schedule:
        pid = p['pid']
        start_time = p['start']
        duration = p['end'] - p['start']
        y_pos = pid_to_index[pid]
        
        # Color based on process index
        color_idx = pid_to_index[pid] % len(modern_colors)
        color = modern_colors[color_idx]
        
        # Shadow effect
        shadow_offset = 0.02
        ax.barh(y_pos - shadow_offset, duration, left=start_time + shadow_offset * max_time, 
                height=0.65, color='black', alpha=0.2, zorder=1)
        
        # Main bar with gradient effect
        bar = ax.barh(y_pos, duration, left=start_time, height=0.65, 
                     color=color, edgecolor='white', linewidth=2.5, 
                     alpha=0.9, zorder=2)
        
        # Inner glow effect
        ax.barh(y_pos, duration * 0.95, left=start_time + duration * 0.025, 
               height=0.55, color='white', alpha=0.15, zorder=3)
        
        # Process label inside bar with background
        if duration > max_time * 0.04:
            label_x = start_time + duration/2
            # Background for text
            bbox_props = dict(boxstyle='round,pad=0.4', facecolor=color, 
                            edgecolor='white', linewidth=1.5, alpha=0.95)
            ax.text(label_x, y_pos, f'{pid}', 
                   ha='center', va='center', 
                   fontsize=12, fontweight='bold', color='white',
                   bbox=bbox_props, zorder=4)
        
        # Enhanced time markers
        # Start time
        ax.plot([start_time, start_time], [y_pos - 0.4, y_pos + 0.4], 
               color='#60a5fa', linewidth=2, linestyle='--', alpha=0.6, zorder=1)
        ax.text(start_time, y_pos - 0.5, f'{start_time:.0f}', 
               ha='center', va='top', fontsize=10, fontweight='bold',
               color='#60a5fa', bbox=dict(boxstyle='round,pad=0.3', 
               facecolor='#1e293b', edgecolor='#60a5fa', linewidth=1))
        
        # End time
        ax.plot([p['end'], p['end']], [y_pos - 0.4, y_pos + 0.4], 
               color='#94a3b8', linewidth=2, linestyle='--', alpha=0.6, zorder=1)
        ax.text(p['end'], y_pos - 0.5, f"{p['end']:.0f}", 
               ha='center', va='top', fontsize=10, fontweight='bold',
               color='#94a3b8', bbox=dict(boxstyle='round,pad=0.3',
               facecolor='#1e293b', edgecolor='#94a3b8', linewidth=1))
    
    # Enhanced Y-axis labels
    ax.set_yticks(range(num_processes))
    y_labels = [f'Process {pid}' for pid in process_ids]
    ax.set_yticklabels(y_labels, fontsize=13, fontweight='bold', color='#e0f2fe')
    
    # Styled axes labels
    ax.set_xlabel('Time (milliseconds)', fontsize=16, fontweight='bold', 
                  color='#94a3b8', labelpad=15)
    ax.set_ylabel('Processes', fontsize=16, fontweight='bold', 
                  color='#94a3b8', labelpad=15)
    
    # Modern title with icon
    ax.set_title('📊 CPU Scheduling Timeline (Gantt Chart)', 
                fontsize=26, fontweight='bold', pad=30,
                color='#e0f2fe', family='sans-serif')
    
    # Enhanced grid
    ax.grid(axis='x', linestyle='--', alpha=0.2, color='#475569', linewidth=1.5)
    ax.set_axisbelow(True)
    
    # Clean spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#475569')
        ax.spines[spine].set_linewidth(2)
    
    # Style tick parameters
    ax.tick_params(colors='#94a3b8', labelsize=11, width=2, length=6)
    
    # Add padding and set limits
    ax.set_xlim(-max_time * 0.02, max_time * 1.08)
    ax.set_ylim(-0.8, num_processes - 0.2)
    
    # Add metadata box
    total_time = max_time
    avg_duration = np.mean([p['end'] - p['start'] for p in process_schedule])
    
    info_text = f'Total Time: {total_time:.0f}ms  |  Processes: {num_processes}  |  Avg Duration: {avg_duration:.1f}ms'
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
           fontsize=11, fontweight='bold', color='#94a3b8',
           va='top', ha='left',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='#0f172a', 
                    edgecolor='#3b82f6', linewidth=2, alpha=0.9))

    plt.tight_layout(pad=2)
    plt.savefig('gantt_chart.png', dpi=300, bbox_inches='tight', 
                facecolor='#0f172a')
    print("✅ Saved: gantt_chart.png")
    
    fig.canvas.manager.set_window_title('⏱️ CPU Scheduling Gantt Chart')
    plt.show(block=True)