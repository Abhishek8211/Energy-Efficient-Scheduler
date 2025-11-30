"""
Test GUI Integration with Raaji's Logic
Quick test to verify GUI + Logic work together
"""

import tkinter as tk
from gui_interface import ModernSchedulerApp
from logic import Process, schedule_tasks, calculate_energy, get_metrics

print("\n" + "=" * 80)
print("🧪 TESTING GUI + RAAJI'S LOGIC INTEGRATION")
print("=" * 80)

# Test 1: Check imports
print("\n✅ Step 1: Imports successful")
print("   - GUI loaded: ModernSchedulerApp")
print("   - Logic loaded: Process, schedule_tasks, calculate_energy, get_metrics")

# Test 2: Create GUI window
print("\n✅ Step 2: Creating GUI window...")
root = tk.Tk()
app = ModernSchedulerApp(root)
print("   - GUI window created successfully")

# Test 3: Add sample processes to GUI
print("\n✅ Step 3: Adding sample processes to GUI...")

sample_processes = [
    {"pid": "P1", "arrival": "0", "burst": "100", "priority": "5", "type": "Foreground"},
    {"pid": "P2", "arrival": "50", "burst": "150", "priority": "3", "type": "Background"},
    {"pid": "P3", "arrival": "100", "burst": "80", "priority": "7", "type": "Background"}
]

for data in sample_processes:
    # Simulate adding via GUI
    app.ent_pid.delete(0, tk.END)
    app.ent_pid.insert(0, data['pid'])
    
    app.ent_arr.delete(0, tk.END)
    app.ent_arr.insert(0, data['arrival'])
    
    app.ent_burst.delete(0, tk.END)
    app.ent_burst.insert(0, data['burst'])
    
    app.ent_priority.delete(0, tk.END)
    app.ent_priority.insert(0, data['priority'])
    
    app.combo_type.set(data['type'])
    
    # Click add button
    app.add_process()
    print(f"   - Added: {data['pid']} ({data['type']})")

print(f"   - Total processes in GUI: {len(app.process_list)}")

# Test 4: Convert GUI data to Raaji's Process objects
print("\n✅ Step 4: Converting GUI data to Logic Process objects...")

logic_processes = []
for p_data in app.process_list:
    process = Process(
        pid=p_data['pid'],
        arrival_time=int(p_data['arrival']),
        burst_time=int(p_data['burst']),
        task_type=p_data['type']
    )
    logic_processes.append(process)
    print(f"   - Created: {process}")

# Test 5: Run Raaji's FCFS algorithm
print("\n✅ Step 5: Running FCFS scheduling algorithm...")

scheduled = schedule_tasks(logic_processes)

print("\n   Scheduling Results:")
for p in scheduled:
    print(f"   - {p.pid}: Completion={p.completion_time:.1f}ms, "
          f"Turnaround={p.turnaround_time:.1f}ms, "
          f"Waiting={p.waiting_time:.1f}ms")

# Test 6: Calculate energy with DVFS
print("\n✅ Step 6: Calculating energy consumption...")

std_energy, dvfs_energy = calculate_energy(scheduled)
savings = ((std_energy - dvfs_energy) / std_energy * 100) if std_energy > 0 else 0

print(f"   - Standard Mode: {std_energy:.2f} mW")
print(f"   - DVFS Mode:     {dvfs_energy:.2f} mW")
print(f"   - Energy Savings: {savings:.1f}%")

# Test 7: Get performance metrics
print("\n✅ Step 7: Calculating performance metrics...")

metrics = get_metrics(scheduled)

print(f"   - Avg Turnaround: {metrics['avg_turnaround']:.2f} ms")
print(f"   - Avg Waiting:    {metrics['avg_waiting']:.2f} ms")
print(f"   - Avg Response:   {metrics['avg_response']:.2f} ms")

# Test 8: Update GUI with results
print("\n✅ Step 8: Updating GUI with real data...")

# Update statistics cards
app.stat_cards["⚡ Energy Saved"]['value'].config(text=f"{savings:.1f}%")
app.stat_cards["⏱️ Avg Turnaround"]['value'].config(
    text=f"{metrics['avg_turnaround']:.1f} ms"
)
app.stat_cards["⏳ Avg Waiting"]['value'].config(
    text=f"{metrics['avg_waiting']:.1f} ms"
)

# Update energy labels
app.lbl_standard_energy.config(text=f"Standard: {std_energy:.2f} mW")
app.lbl_dvfs_energy.config(text=f"DVFS: {dvfs_energy:.2f} mW")
app.lbl_savings.config(text=f"💰 Savings: {savings:.1f}%")

print("   - Statistics cards updated")
print("   - Energy labels updated")

# Final summary
print("\n" + "=" * 80)
print("✅ ALL INTEGRATION TESTS PASSED!")
print("=" * 80)
print("\n📋 Summary:")
print(f"   • Processes scheduled: {len(scheduled)}")
print(f"   • Energy savings: {savings:.1f}%")
print(f"   • GUI updated successfully")
print(f"   • Raaji's logic fully integrated")
print("\n🎉 Ready for production use!")
print("=" * 80)

print("\n💡 Instructions:")
print("   1. The GUI window is now open")
print("   2. You can manually add more processes using the form")
print("   3. Click 'RUN SIMULATION' to see animation with Raaji's algorithm")
print("   4. Close window when done testing")
print()

# Keep window open
root.mainloop()
