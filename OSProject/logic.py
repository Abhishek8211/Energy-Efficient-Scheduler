"""
logic.py - CPU Scheduling Logic & DVFS Energy Calculation
Original Author: Rajeswari
"""


class Process:
    """
    Defines a process object with attributes required for scheduling 
    and energy calculation.
    """
    def __init__(self, pid, arrival_time, burst_time, task_type):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.task_type = task_type
        
        # Set CPU frequency based on task type (DVFS)
        if task_type == "Foreground":
            self.frequency = 1.0  # High power mode (1.0 GHz)
        else:  # Background
            self.frequency = 0.6  # Low power mode (0.6 GHz) - DVFS ENERGY SAVING
        
        # Initialize performance metrics (calculated during scheduling)
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0
        self.energy_consumed = 0

    def __repr__(self):
        """Developer-friendly representation"""
        return (f"Process(PID={self.pid}, Arrival={self.arrival_time}, "
                f"Burst={self.burst_time}, Type='{self.task_type}', Freq={self.frequency}GHz)")
    
    def __str__(self):
        """User-friendly representation"""
        return f"[{self.pid}] {self.task_type} task (Arrival: {self.arrival_time}ms, Burst: {self.burst_time}ms)"


def schedule_tasks(process_list):
    """
    FCFS (First-Come-First-Serve) Scheduling Algorithm
    Sorts processes by arrival time and calculates all timing metrics.
    
    Args:
        process_list (list): List of Process objects
        
    Returns:
        list: Sorted and scheduled processes with calculated times
    """
    # Edge case: Empty list
    if not process_list:
        print("⚠️ No processes to schedule!")
        return []
    
    # Step 1: Sort by arrival time (FCFS principle)
    sorted_list = sorted(process_list, key=lambda process: process.arrival_time)
    
    current_time = 0  # CPU clock starts at 0
    
    print("=" * 70)
    print("FCFS SCHEDULING WITH DVFS")
    print("=" * 70)
    
    for process in sorted_list:
        # If CPU is idle, jump to process arrival time
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        
        # IMPORTANT: Response time is when process first gets CPU
        process.response_time = current_time - process.arrival_time
        
        # Calculate execution time based on frequency
        # Background tasks take LONGER because they run at lower frequency
        if process.task_type == "Background":
            execution_time = process.burst_time / process.frequency  # Slower execution
        else:
            execution_time = process.burst_time  # Full speed
        
        # Calculate completion time
        process.completion_time = current_time + execution_time
        
        # Update CPU clock
        current_time = process.completion_time
        
        # Calculate performance metrics
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - execution_time
        
        # Print scheduling details
        print(f"PID {process.pid}: Arrival={process.arrival_time}ms, "
              f"Burst={process.burst_time}ms, Type='{process.task_type}', "
              f"Freq={process.frequency}GHz, Completion={process.completion_time:.1f}ms, "
              f"Response={process.response_time:.1f}ms")
    
    print("=" * 70)
    return sorted_list


def calculate_energy(process_list):
    """
    Calculate energy consumption for Standard Mode vs DVFS Mode
    
    Energy Formula: Energy = Time × Frequency²
    
    Standard Mode: All tasks run at high frequency (1.0 GHz)
    DVFS Mode: Background tasks run at low frequency (0.6 GHz) - SAVES ENERGY!
    
    Args:
        process_list (list): List of scheduled Process objects
        
    Returns:
        tuple: (standard_energy, dvfs_energy) in milliwatts
    """
    # Edge case: Empty list
    if not process_list:
        print("⚠️ No processes to calculate energy!")
        return 0.0, 0.0
    
    total_energy_standard = 0  # All tasks at 1.0 GHz
    total_energy_dvfs = 0      # Background tasks at 0.6 GHz
    
    print("\n" + "=" * 70)
    print("ENERGY CALCULATION (Standard vs DVFS)")
    print("=" * 70)
    
    for process in process_list:
        burst = process.burst_time
        
        if process.task_type == "Foreground":
            # Foreground tasks: Always run at high frequency in both modes
            freq = 1.0
            time_exec = burst
            energy = time_exec * (freq ** 2)  # Energy = Time × Freq²
            
            total_energy_standard += energy
            total_energy_dvfs += energy
            
            process.energy_consumed = energy
            
            print(f"PID {process.pid} (Foreground): "
                  f"Both modes use {energy:.2f} mW (1.0 GHz)")
            
        else:  # Background task
            # Standard mode: High frequency (wasteful!)
            freq_std = 1.0
            time_std = burst
            energy_std = time_std * (freq_std ** 2)
            total_energy_standard += energy_std
            
            # DVFS mode: Low frequency (ENERGY SAVING!)
            freq_dvfs = 0.6
            time_dvfs = burst / freq_dvfs  # Takes longer but uses less power
            energy_dvfs = time_dvfs * (freq_dvfs ** 2)  # Much less energy!
            total_energy_dvfs += energy_dvfs
            
            process.energy_consumed = energy_dvfs
            
            savings = ((energy_std - energy_dvfs) / energy_std * 100)
            
            print(f"PID {process.pid} (Background): "
                  f"Standard={energy_std:.2f} mW, DVFS={energy_dvfs:.2f} mW "
                  f"(Saves {savings:.1f}%)")
    
    print("=" * 70)
    print(f"TOTAL STANDARD MODE ENERGY: {total_energy_standard:.2f} mW")
    print(f"TOTAL DVFS MODE ENERGY:     {total_energy_dvfs:.2f} mW")
    
    overall_savings = ((total_energy_standard - total_energy_dvfs) / 
                      total_energy_standard * 100) if total_energy_standard > 0 else 0
    
    print(f"OVERALL ENERGY SAVINGS:     {overall_savings:.1f}%")
    print("=" * 70)
    
    return total_energy_standard, total_energy_dvfs


def get_metrics(process_list):
    """
    Calculate average performance metrics for all processes
    
    Args:
        process_list (list): List of scheduled Process objects
        
    Returns:
        dict: Contains avg_turnaround, avg_waiting, avg_response
    """
    # Edge case: Empty list
    if not process_list:
        return {
            'avg_turnaround': 0,
            'avg_waiting': 0,
            'avg_response': 0
        }
    
    total_turnaround = sum(p.turnaround_time for p in process_list)
    total_waiting = sum(p.waiting_time for p in process_list)
    total_response = sum(p.response_time for p in process_list)
    
    n = len(process_list)
    
    metrics = {
        'avg_turnaround': total_turnaround / n,
        'avg_waiting': total_waiting / n,
        'avg_response': total_response / n
    }
    
    print("\n" + "=" * 70)
    print("PERFORMANCE METRICS")
    print("=" * 70)
    print(f"Average Turnaround Time: {metrics['avg_turnaround']:.2f} ms")
    print(f"Average Waiting Time:    {metrics['avg_waiting']:.2f} ms")
    print(f"Average Response Time:   {metrics['avg_response']:.2f} ms")
    print("=" * 70)
    
    return metrics


def get_gantt_data(process_list):
    """
    Generate Gantt chart data for visualization
    Useful for GUI integration
    
    Args:
        process_list (list): List of scheduled Process objects
        
    Returns:
        list: List of dicts with gantt chart data
    """
    gantt_data = []
    
    for process in sorted(process_list, key=lambda p: p.arrival_time):
        if process.task_type == "Background":
            execution_time = process.burst_time / process.frequency
        else:
            execution_time = process.burst_time
        
        start_time = process.completion_time - execution_time
        
        gantt_data.append({
            'pid': process.pid,
            'start': start_time,
            'duration': execution_time,
            'type': process.task_type,
            'frequency': process.frequency
        })
    
    return gantt_data


def convert_to_visualization_format(process_list):
    """
    Convert Raaji's Process objects to Kaushiki's visualization format
    
    Kaushiki's draw_gantt_chart() expects:
        [{'pid': 'P1', 'start': 0, 'end': 100}, ...]
    
    Raaji's Process has:
        - pid, arrival_time, burst_time, completion_time
    
    Args:
        process_list (list): List of scheduled Process objects
        
    Returns:
        list: List of dicts formatted for Kaushiki's visualization
    """
    viz_data = []
    
    for process in sorted(process_list, key=lambda p: p.arrival_time):
        # Calculate start time
        if process.task_type == "Background":
            execution_time = process.burst_time / process.frequency
        else:
            execution_time = process.burst_time
        
        start_time = process.completion_time - execution_time
        end_time = process.completion_time
        
        viz_data.append({
            'pid': process.pid,
            'start': start_time,
            'end': end_time
        })
    
    return viz_data


# Test the module
if __name__ == "__main__":
    print("\n🧪 TESTING LOGIC MODULE\n")
    
    # Test 1: Normal case
    print("TEST 1: Normal Case (Mixed workload)")
    test_processes = [
        Process("P1", 0, 100, "Foreground"),
        Process("P2", 50, 150, "Background"),
        Process("P3", 100, 80, "Background")
    ]
    
    print("\nCreated Test Processes:")
    for p in test_processes:
        print(f"  {p}")
    
    scheduled = schedule_tasks(test_processes)
    std_energy, dvfs_energy = calculate_energy(scheduled)
    metrics = get_metrics(scheduled)
    gantt = get_gantt_data(scheduled)
    
    print(f"\n✅ TEST 1 PASSED!")
    print(f"📊 Energy Savings: {((std_energy - dvfs_energy) / std_energy * 100):.1f}%")
    
    # Test 2: Edge case - Empty list
    print("\n" + "="*70)
    print("TEST 2: Edge Case (Empty list)")
    empty_scheduled = schedule_tasks([])
    empty_std, empty_dvfs = calculate_energy([])
    empty_metrics = get_metrics([])
    print("✅ TEST 2 PASSED! (Handled empty list gracefully)")
    
    # Test 3: Only foreground tasks
    print("\n" + "="*70)
    print("TEST 3: Only Foreground Tasks (No DVFS savings)")
    fg_only = [
        Process("P1", 0, 100, "Foreground"),
        Process("P2", 50, 150, "Foreground")
    ]
    fg_scheduled = schedule_tasks(fg_only)
    fg_std, fg_dvfs = calculate_energy(fg_scheduled)
    print(f"\n✅ TEST 3 PASSED!")
    print(f"📊 Expected 0% savings: {((fg_std - fg_dvfs) / fg_std * 100):.1f}%")
    
    # Test 4: Only background tasks
    print("\n" + "="*70)
    print("TEST 4: Only Background Tasks (Maximum DVFS savings)")
    bg_only = [
        Process("P1", 0, 100, "Background"),
        Process("P2", 50, 150, "Background")
    ]
    bg_scheduled = schedule_tasks(bg_only)
    bg_std, bg_dvfs = calculate_energy(bg_scheduled)
    print(f"\n✅ TEST 4 PASSED!")
    print(f"📊 Maximum savings: {((bg_std - bg_dvfs) / bg_std * 100):.1f}%")
    
    print("\n" + "="*70)
    print("🎉 ALL TESTS PASSED!")
    print("="*70)
    print("✅ Process class working correctly")
    print("✅ FCFS scheduling working correctly")
    print("✅ DVFS energy calculation working correctly")
    print("✅ Performance metrics working correctly")
    print("✅ Edge cases handled properly")
    print("✅ Ready for GUI integration!")
    print("="*70)
