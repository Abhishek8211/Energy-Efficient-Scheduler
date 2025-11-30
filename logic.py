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
# logic.py (Add this function below the Process class)

def schedule_tasks(process_list):
    """
    Simulates FCFS by sorting the list of processes based on Arrival Time.
    This is the first step of the core logic.
    """
    # Use the Python 'sorted' function with a lambda function as the key.
    # The key tells Python to compare elements based on the 'arrival' attribute
    # of the Process object.
    sorted_list = sorted(process_list, key=lambda process: process.arrival)
    
    print("Processes sorted by Arrival Time (FCFS):")
    for process in sorted_list:
        # Using the __repr__ method added in Commit 1 for clear output
        print(process)
        
    return sorted_list
    
# You can test this by adding a small example block to the bottom of logic.py temporarily:
# if __name__ == '__main__':
#     p1 = Process(1, 4, 10, 'Foreground')
#     p2 = Process(2, 0, 5, 'Background')
#     p3 = Process(3, 2, 8, 'Foreground')
#     
#     unsorted_list = [p1, p2, p3]
#     print("Unsorted List:")
#     for p in unsorted_list:
#         print(p)
#     
#     scheduled_list = schedule_tasks(unsorted_list)