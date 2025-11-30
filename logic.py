# logic.py

class Process:
    """
    Defines a process object with attributes required for scheduling 
    and energy calculation.
    """
    def __init__(self, pid, arrival, burst, type):
        # Store attributes from the constructor
        self.pid = pid          # Process ID
        self.arrival = arrival  # Arrival Time (when the process enters the queue)
        self.burst = burst      # Burst Time (CPU time required for execution)
        self.type = type        # Task Type (Foreground or Background)
        
        # Initialize results/status variables (to be used in later commits)
        self.start_time = 0
        self.finish_time = 0
        self.energy_consumed = 0

    def __repr__(self):
        """
        A helper method for easily viewing the process details in a list.
        """
        return (f"Process(PID={self.pid}, Arrival={self.arrival}, "
                f"Burst={self.burst}, Type='{self.type}')")

# Example usage (Optional, for testing the class structure):
# p1 = Process(1, 0, 10, 'Foreground')
# print(p1)