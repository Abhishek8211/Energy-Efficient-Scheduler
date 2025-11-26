# ⚡ Energy-Efficient CPU Scheduler

**DVFS-Based Scheduling System for Mobile Computing**

## 👥 Team Members
- **Abhishek** - GUI & Integration (`gui_interface.py`)
- **Raaji** - Logic & Algorithms (`logic.py`)
- **Kaushiki** - Data Visualization (`visualization.py`)

## 🎯 Project Goal
Develop a CPU scheduling algorithm that minimizes energy consumption by 25-40% using Dynamic Voltage Frequency Scaling (DVFS) without compromising performance.

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone <your-repo-url>
cd OSProject

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Testing
```bash
python test_integration.py
```

## 📊 Features
- ✅ FCFS Scheduling with DVFS
- ✅ Real-time Gantt chart animation
- ✅ Energy consumption analysis
- ✅ Scientific matplotlib visualizations
- ✅ CSV import/export
- ✅ Dark/Light theme support
- ✅ Keyboard shortcuts

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         GUI Layer (Abhishek)            │
│  • User input & display                 │
│  • Real-time animations                 │
│  • Theme management                     │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      Logic Layer (Rajeswari)                │
│  • Process class                        │
│  • FCFS scheduling                      │
│  • DVFS energy calculation              │
│  • Energy = Time × Frequency²           │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│    Visualization Layer (Kaushiki)       │
│  • Matplotlib scientific plots          │
│  • Energy comparison charts             │
│  • Gantt chart diagrams                 │
└─────────────────────────────────────────┘
```

## 📦 Project Structure
```
OSProject/
├── gui_interface.py      # Abhishek's GUI module
├── logic.py              # Raaji's algorithm module
├── visualization.py      # Kaushiki's visualization module
├── main.py               # Integration file
├── test_integration.py   # Testing suite
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## 🎮 Usage

1. **Add Processes:**
   - Enter Process ID, Arrival Time, Burst Time
   - Select Task Type (Foreground/Background)
   - Click "ADD TASK"

2. **Run Simulation:**
   - Click "RUN SIMULATION"
   - Watch real-time Gantt chart animation
   - View energy savings

3. **Export Results:**
   - Click "EXPORT REPORT"
   - CSV file generated with full analysis

## ⌨️ Keyboard Shortcuts
- `Ctrl+I` - Import CSV
- `Ctrl+E` - Export Report
- `Ctrl+D` - Clear All
- `Ctrl+R` / `F5` - Run Simulation
- `Ctrl+T` - Toggle Theme
- `F1` - Help

## 📈 Expected Results
- **Energy Savings:** 25-40% for mixed workloads
- **Performance:** Similar turnaround time to standard scheduling
- **Efficiency:** Best for background-heavy workloads

## 🧪 Testing
All modules tested individually and integrated:
- ✅ Unit tests for Process class
- ✅ FCFS algorithm validation
- ✅ Energy calculation accuracy
- ✅ Visualization output
- ✅ GUI integration

## 📜 License
Educational Project - LPU CSE316

## 📞 Support
For issues, contact ***
