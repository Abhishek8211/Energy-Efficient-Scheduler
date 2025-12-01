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