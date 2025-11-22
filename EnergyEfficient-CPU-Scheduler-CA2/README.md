# Energy-Efficient CPU Scheduling Algorithm

### Course: CSE316 - Operating Systems (Project CA2)
### Team Members:
- Abhishek (Scheduler Core)
- Kaushiki (Simulator & Analysis)
- Rajeswari (Documentation & Report)

---

## 🧠 Overview
This project implements an **Energy-Efficient CPU Scheduling Algorithm** that minimizes energy consumption without compromising performance.  
The scheduler uses **Earliest Deadline First (EDF)** combined with **Dynamic Voltage and Frequency Scaling (DVFS)** and **Slack Reclamation** to dynamically adjust CPU speed based on workload demand.

---

## 📁 Folder Structure
```
src/             → Python source code (scheduler, simulator, energy model)
experiments/     → Workload configs, scripts, and results
report/          → Final report, flow diagram, and appendix
presentation/    → Project presentation slides
```

---

## 🧩 Branch & Revision Plan

### Branches
| Member | Branch Name | Responsibility |
|---------|--------------|----------------|
| Abhishek | feature/abhishek-scheduler | Core scheduling algorithm |
| Kaushiki | feature/kaushiki-simulator | Simulator and analysis scripts |
| Rajeswari | feature/rajeswari-report | Documentation and presentation |

### Commit Plan (7 commits each)
Each member must make **7 meaningful commits**:
- Abhishek: Scheduler + DVFS + Testing
- Kaushiki: Simulator + Energy model + Plots
- Rajeswari: Report + Flow diagram + Slides

Use clear commit messages like:
```
feat: add DVFS scheduler logic
fix: corrected energy model calculation
docs: added flow diagram to report
```

---

## ⚙️ How to Start
1. One member (Abhishek) creates a **GitHub repository** named `EnergyEfficient-CPU-Scheduler-CA2`.
2. Add **Kaushiki** and **Rajeswari** as collaborators.
3. Each member clones the repo:
   ```bash
   git clone <repo-link>
   cd EnergyEfficient-CPU-Scheduler-CA2
   ```
4. Each member creates their own branch:
   ```bash
   git checkout -b feature/<your-name>-branch
   ```
5. Add files or code to your section, commit, and push:
   ```bash
   git add .
   git commit -m "feat: added initial simulator structure"
   git push origin feature/<your-name>-branch
   ```
6. Repeat for 7 meaningful commits each.
7. Open Pull Requests (PRs) to merge your branch into `main`.

---

## 🧾 Example Revision Log Table (for report)
| Member | Branch | No. of Commits | Example Commit Messages |
|---------|---------|----------------|--------------------------|
| Abhishek | feature/abhishek-scheduler | 7 | feat: implement EDF logic |
| Kaushiki | feature/kaushiki-simulator | 7 | feat: add energy model |
| Rajeswari | feature/rajeswari-report | 7 | docs: add final report |

---

## 🧩 Next Steps After Setup
After pushing this structure to GitHub:
1. Start writing actual Python code in `src/`.
2. Keep committing as you make progress.
3. Run local tests and record results in `experiments/results/`.
4. Prepare your report and presentation in the corresponding folders.
5. Ensure all members have **7 commits each** visible in the Git history.
6. Merge all branches into `main` for final submission.

---

## 📜 License
This project is created as part of **CSE316 Operating Systems Project (CA2)**.
