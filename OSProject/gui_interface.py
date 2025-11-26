from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import csv
import datetime
import random
import math
import time

class ModernSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Energy-Efficient Scheduler | Team Abhi")
        self.root.geometry("1200x850")
        self.root.minsize(1000, 700)
        
        # --- ENHANCED THEME CONFIGURATIONS ---
        self.themes = {
            "dark": {
                "bg": "#0a0e27",
                "bg_gradient": "#1a1d3a",
                "panel": "#1e2139",
                "panel_hover": "#252847",
                "text": "#ffffff",
                "input_bg": "#2d3250",
                "green": "#00ff88",
                "blue": "#00d4ff",
                "purple": "#b388ff",
                "red": "#ff5370",
                "orange": "#ffaa00",
                "yellow": "#ffd500",
                "fg_secondary": "#8b92b8",
                "btn_text": "#ffffff",
                "shadow": "#000000",
                "success": "#00ff88",
                "warning": "#ffaa00",
                "error": "#ff5370"
            },
            "light": {
                "bg": "#fef9e7",
                "bg_gradient": "#fef5d4",
                "panel": "#fffef8",
                "panel_hover": "#fffcf0",
                "text": "#2d2416",
                "input_bg": "#fffef9",
                "green": "#16a34a",
                "blue": "#0284c7",
                "purple": "#7c3aed",
                "red": "#dc2626",
                "orange": "#ea580c",
                "yellow": "#ca8a04",
                "fg_secondary": "#78716c",
                "btn_text": "#ffffff",
                "shadow": "#d6d3d1",
                "success": "#16a34a",
                "warning": "#ea580c",
                "error": "#dc2626"
            }
        }
        
        self.current_mode = "dark"
        self.colors = self.themes[self.current_mode]
        
        self.process_list = []
        self.simulation_running = False
        self.animation_id = None
        
        self.setup_styles()
        self.create_menu_bar()
        self.create_background_particles()
        self.create_widgets()
        self.create_cpu_meter()
        self.apply_theme()
        self.start_idle_animation()
        self.bind_keyboard_shortcuts()

    def setup_styles(self):
        """Enhanced TTK styles"""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.map("Treeview", 
                      background=[('selected', self.colors["blue"])],
                      foreground=[('selected', '#ffffff')])
        
        self.style.configure("Custom.TNotebook", background=self.colors["bg"])
        self.style.configure("Custom.TNotebook.Tab", 
                           padding=[20, 10], 
                           font=("Segoe UI", 10, "bold"))
    
    def create_menu_bar(self):
        """Professional menu bar"""
        menubar = tk.Menu(self.root, font=("Segoe UI", 9))
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 9))
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="📥 Import CSV", command=self.import_csv, accelerator="Ctrl+I")
        file_menu.add_command(label="📤 Export Report", command=self.export_data, accelerator="Ctrl+E")
        file_menu.add_command(label="💾 Save Project", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="🗑️ Clear All", command=self.clear_all, accelerator="Ctrl+D")
        file_menu.add_separator()
        file_menu.add_command(label="❌ Exit", command=self.root.quit)
        
        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 9))
        menubar.add_cascade(label="👁️ View", menu=view_menu)
        view_menu.add_command(label="🌗 Toggle Theme", command=self.toggle_theme, accelerator="Ctrl+T")
        view_menu.add_command(label="📊 Statistics Dashboard", command=self.show_statistics)
        view_menu.add_command(label="📈 Performance Graph", command=self.show_performance_graph)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 9))
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="📖 User Guide", command=self.show_help)
        help_menu.add_command(label="ℹ️ About", command=self.show_about)
        
        # Keyboard shortcuts
        self.root.bind('<Control-i>', lambda e: self.import_csv())
        self.root.bind('<Control-e>', lambda e: self.export_data())
        self.root.bind('<Control-d>', lambda e: self.clear_all())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())

    def create_widgets(self):
        """Modern UI components"""
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 1. HEADER
        self.header_frame = tk.Frame(main_container, height=120)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        self.header_frame.pack_propagate(False)
        
        title_container = tk.Frame(self.header_frame)
        title_container.place(relx=0.5, rely=0.35, anchor="center")
        
        self.title_label = tk.Label(title_container, text="⚡ CPU ENERGY OPTIMIZER", 
                                    font=("Segoe UI", 28, "bold"))
        self.title_label.pack()
        
        self.subtitle_label = tk.Label(title_container, 
                                       text="🔋 DVFS-Based Scheduling • Real-Time Power Management • Mobile Systems", 
                                       font=("Segoe UI", 10, "italic"))
        self.subtitle_label.pack(pady=(5, 0))

        self.btn_theme = tk.Button(self.header_frame, text="🌙 LIGHT", 
                                   command=self.toggle_theme, relief="flat", 
                                   font=("Segoe UI", 9, "bold"),
                                   cursor="hand2", padx=20, pady=8, bd=0)
        self.btn_theme.place(relx=0.97, rely=0.5, anchor="e")

        self.create_battery_widget()
        self.create_status_indicator()
        
        # Lower particle canvas to background
        if hasattr(self, 'particle_canvas'):
            try:
                self.particle_canvas.lower(self.header_frame)
            except:
                pass
        
        # 2. STATISTICS CARDS
        self.create_stats_dashboard(main_container)

        # 3. INPUT PANEL
        self.create_input_panel(main_container)

        # 4. ACTION BUTTONS
        self.create_action_buttons(main_container)

        # 5. TABBED INTERFACE
        self.create_tabbed_interface(main_container)

    def create_stats_dashboard(self, parent):
        """Animated statistics cards"""
        stats_container = tk.Frame(parent)
        stats_container.pack(fill=tk.X, pady=(0, 15))
        
        stats = [
            ("📋 Total Tasks", "0", "green"),
            ("⏱️ Avg Turnaround", "0 ms", "blue"),
            ("⏳ Avg Waiting", "0 ms", "orange"),
            ("⚡ Energy Saved", "0%", "purple")
        ]
        
        self.stat_cards = {}
        for i, (title, value, color_key) in enumerate(stats):
            card = tk.Frame(stats_container, relief="flat", bd=0)
            card.grid(row=0, column=i, padx=8, sticky="ew")
            stats_container.columnconfigure(i, weight=1)
            
            lbl_title = tk.Label(card, text=title, font=("Segoe UI", 9, "bold"))
            lbl_title.pack(pady=(10, 2))
            
            lbl_value = tk.Label(card, text=value, font=("Segoe UI", 20, "bold"))
            lbl_value.pack(pady=(0, 10))
            
            self.stat_cards[title] = {
                'frame': card,
                'value': lbl_value,
                'title': lbl_title,
                'color': color_key
            }
            
            card.bind("<Enter>", lambda e, c=card: self.card_hover(c, True))
            card.bind("<Leave>", lambda e, c=card: self.card_hover(c, False))

    def card_hover(self, card, entering):
        """Card hover animation"""
        if entering:
            card.config(relief="raised", bd=2)
        else:
            card.config(relief="flat", bd=0)

    def create_input_panel(self, parent):
        """Modern input panel"""
        input_container = tk.Frame(parent)
        input_container.pack(fill=tk.X, pady=(0, 15))
        
        self.input_frame = tk.Frame(input_container, bd=0, highlightthickness=2)
        self.input_frame.pack(fill=tk.X, padx=5)
        
        title_bar = tk.Frame(self.input_frame)
        title_bar.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        tk.Label(title_bar, text="➕ ADD NEW PROCESS", 
                font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT)
        tk.Label(title_bar, text="Configure task parameters below", 
                font=("Segoe UI", 9, "italic")).pack(side=tk.LEFT, padx=10)
        
        input_grid = tk.Frame(self.input_frame)
        input_grid.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        def create_input(icon, label_text, col, placeholder=""):
            container = tk.Frame(input_grid)
            container.grid(row=0, column=col, padx=12, sticky="ew")
            input_grid.columnconfigure(col, weight=1)
            
            lbl = tk.Label(container, text=f"{icon} {label_text}", 
                          font=("Segoe UI", 9, "bold"))
            lbl.pack(anchor="w", pady=(0, 6))
            
            ent = tk.Entry(container, relief="flat", font=("Segoe UI", 11), 
                          bd=2, insertwidth=2)
            ent.pack(fill=tk.X, ipady=8)
            
            if placeholder:
                ent.insert(0, placeholder)
                ent.bind("<FocusIn>", lambda e: ent.delete(0, tk.END) if ent.get() == placeholder else None)
            
            return lbl, ent

        self.lbl_pid, self.ent_pid = create_input("🆔", "PROCESS ID", 0, "P101")
        self.lbl_arr, self.ent_arr = create_input("🕐", "ARRIVAL (ms)", 1, "0")
        self.lbl_burst, self.ent_burst = create_input("⏱️", "BURST (ms)", 2, "100")
        self.lbl_priority, self.ent_priority = create_input("🎯", "PRIORITY", 3, "5")
        
        type_container = tk.Frame(input_grid)
        type_container.grid(row=0, column=4, padx=12, sticky="ew")
        input_grid.columnconfigure(4, weight=1)
        
        self.lbl_type = tk.Label(type_container, text="⚙️ TASK TYPE", 
                                font=("Segoe UI", 9, "bold"))
        self.lbl_type.pack(anchor="w", pady=(0, 6))
        
        self.var_type = tk.StringVar(value="Foreground")
        self.combo_type = ttk.Combobox(type_container, textvariable=self.var_type, 
                                       values=["Foreground", "Background"], 
                                       state="readonly", font=("Segoe UI", 10))
        self.combo_type.pack(fill=tk.X, ipady=6)

    def create_action_buttons(self, parent):
        """Beautiful gradient buttons"""
        self.btn_frame = tk.Frame(parent)
        self.btn_frame.pack(pady=15)
        
        button_configs = [
            ("➕ ADD TASK", self.add_process, "green"),
            ("▶️ RUN SIMULATION", self.run_simulation, "blue"),
            ("💾 EXPORT REPORT", self.export_data, "orange"),
            ("🔄 RESET ALL", self.clear_all, "red")
        ]
        
        self.action_buttons = {}
        for text, cmd, color_key in button_configs:
            btn = tk.Button(self.btn_frame, text=text, command=cmd, 
                          font=("Segoe UI", 11, "bold"), relief="flat",
                          padx=28, pady=12, cursor="hand2", bd=0)
            btn.pack(side=tk.LEFT, padx=10)
            
            btn.bind("<Enter>", lambda e, b=btn, c=color_key: self.on_button_hover(b, c, True))
            btn.bind("<Leave>", lambda e, b=btn, c=color_key: self.on_button_hover(b, c, False))
            
            self.action_buttons[text] = (btn, color_key)

    def on_button_hover(self, button, color_key, entering):
        """Button hover effect"""
        if entering:
            button.config(relief="raised", bd=2)
        else:
            button.config(relief="flat", bd=0)

    def create_tabbed_interface(self, parent):
        """Tabbed view"""
        notebook = ttk.Notebook(parent, style="Custom.TNotebook")
        notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Tab 1: Process Queue
        table_tab = tk.Frame(notebook)
        notebook.add(table_tab, text="📋 Process Queue")
        self.create_process_table(table_tab)
        
        # Tab 2: Gantt Chart
        gantt_tab = tk.Frame(notebook)
        notebook.add(gantt_tab, text="📊 Gantt Chart")
        self.create_gantt_chart(gantt_tab)
        
        # Tab 3: Energy Analysis
        energy_tab = tk.Frame(notebook)
        notebook.add(energy_tab, text="⚡ Energy Analysis")
        self.create_energy_graph(energy_tab)

    def create_process_table(self, parent):
        """Enhanced table with search"""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        search_frame = tk.Frame(frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="🔍 Search:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Consolas", 10))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_processes)
        
        cols = ("PID", "Arrival", "Burst", "Priority", "Type", "Status")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        
        col_widths = {"PID": 100, "Arrival": 100, "Burst": 100, 
                     "Priority": 80, "Type": 120, "Status": 100}
        
        for col in cols:
            self.tree.heading(col, text=col.upper(), 
                            command=lambda c=col: self.sort_column(c))
            self.tree.column(col, anchor="center", width=col_widths.get(col, 100))
        
        # Table container with scrollbars
        table_container = tk.Frame(frame)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.tag_configure('foreground', background='#ff6b6b', foreground='white')
        self.tree.tag_configure('background', background='#4ecdc4', foreground='white')
        self.tree.tag_configure('completed', background='#95e1d3')
        
        self.tree.bind("<Button-3>", self.show_context_menu)

    def create_gantt_chart(self, parent):
        """Gantt chart visualization"""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="📊 PROCESS EXECUTION TIMELINE", 
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        self.gantt_canvas = tk.Canvas(frame, height=300, bg=self.colors["panel"])
        self.gantt_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        legend_frame = tk.Frame(frame)
        legend_frame.pack(pady=10)
        
        legends = [
            ("🟥 Foreground Tasks", "#ff6b6b"),
            ("🟦 Background Tasks", "#4ecdc4"),
            ("🟩 Completed", "#27ae60")
        ]
        
        for text, color in legends:
            lbl = tk.Label(legend_frame, text=text, font=("Segoe UI", 9))
            lbl.pack(side=tk.LEFT, padx=15)

    def create_energy_graph(self, parent):
        """Energy visualization"""
        frame = tk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="⚡ ENERGY CONSUMPTION ANALYSIS", 
                font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        self.energy_canvas = tk.Canvas(frame, height=300, bg=self.colors["panel"])
        self.energy_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info_frame = tk.Frame(frame)
        info_frame.pack(pady=10)
        
        self.lbl_standard_energy = tk.Label(info_frame, text="Standard: 0 mW", 
                                           font=("Segoe UI", 10, "bold"))
        self.lbl_standard_energy.pack(side=tk.LEFT, padx=20)
        
        self.lbl_dvfs_energy = tk.Label(info_frame, text="DVFS: 0 mW", 
                                       font=("Segoe UI", 10, "bold"))
        self.lbl_dvfs_energy.pack(side=tk.LEFT, padx=20)
        
        self.lbl_savings = tk.Label(info_frame, text="Savings: 0%", 
                                   font=("Segoe UI", 10, "bold"))
        self.lbl_savings.pack(side=tk.LEFT, padx=20)

    def create_battery_widget(self):
        """Animated circular progress ring"""
        self.batt_frame = tk.Frame(self.header_frame)
        self.batt_frame.place(relx=0.02, rely=0.2, anchor="nw")
        
        self.canvas_batt = tk.Canvas(self.batt_frame, width=80, height=80, 
                                    highlightthickness=0, bg=self.colors["bg"])
        self.canvas_batt.pack(side=tk.LEFT)
        
        # Background circle
        self.canvas_batt.create_oval(10, 10, 70, 70, outline=self.colors["fg_secondary"], 
                                    width=6)
        
        # Animated arc (progress)
        self.batt_arc = self.canvas_batt.create_arc(10, 10, 70, 70, 
                                                    start=90, extent=0,
                                                    outline=self.colors["green"], 
                                                    width=6, style='arc')
        
        # Center text
        self.batt_text = self.canvas_batt.create_text(40, 40, text="100%", 
                                                      font=("Segoe UI", 14, "bold"),
                                                      fill=self.colors["green"])
        
        self.lbl_batt_status = tk.Label(self.batt_frame, text="⚡ Full", 
                                       font=("Segoe UI", 9, "bold"),
                                       bg=self.colors["bg"], fg=self.colors["green"])
        self.lbl_batt_status.pack(side=tk.LEFT, padx=8)
        
        self.animate_battery_ring()

    def animate_battery_ring(self, angle=0):
        """Smooth circular animation"""
        target_angle = 360
        if angle < target_angle:
            self.canvas_batt.itemconfig(self.batt_arc, extent=-angle)
            self.root.after(20, lambda: self.animate_battery_ring(angle + 5))

    def create_status_indicator(self):
        """Status indicator"""
        self.status_frame = tk.Frame(self.header_frame)
        self.status_frame.place(relx=0.5, rely=0.9, anchor="center")
        
        self.status_dot = tk.Canvas(self.status_frame, width=12, height=12, 
                                   highlightthickness=0)
        self.status_dot.pack(side=tk.LEFT, padx=5)
        self.dot = self.status_dot.create_oval(2, 2, 10, 10, fill="#27ae60", outline="")
        
        self.lbl_status = tk.Label(self.status_frame, text="Ready", 
                                  font=("Segoe UI", 9, "bold"))
        self.lbl_status.pack(side=tk.LEFT)

    def start_idle_animation(self):
        """Pulsing status dot animation"""
        def pulse():
            try:
                current_color = self.status_dot.itemcget(self.dot, 'fill')
                if current_color == self.colors["green"]:
                    new_color = self.lighten_color(self.colors["green"])
                else:
                    new_color = self.colors["green"]
                self.status_dot.itemconfig(self.dot, fill=new_color)
                self.animation_id = self.root.after(1000, pulse)
            except:
                pass
        pulse()

    def lighten_color(self, hex_color):
        """Lighten hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def create_background_particles(self):
        """Floating particles background"""
        self.particle_canvas = tk.Canvas(self.root, highlightthickness=0, bg=self.colors["bg"])
        self.particle_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        # Will be lowered after main widgets are created
        
        self.particles = []
        for _ in range(25):
            x = random.randint(0, 1200)
            y = random.randint(0, 850)
            size = random.randint(2, 4)
            particle = self.particle_canvas.create_oval(x, y, x+size, y+size, 
                                                        fill=self.colors["blue"], 
                                                        outline="")
            self.particles.append({'id': particle, 'x': x, 'y': y, 'speed': random.uniform(0.3, 1.5)})
        
        self.animate_particles()

    def animate_particles(self):
        """Move particles"""
        try:
            for p in self.particles:
                p['y'] += p['speed']
                if p['y'] > 850:
                    p['y'] = 0
                    p['x'] = random.randint(0, 1200)
                
                self.particle_canvas.coords(p['id'], p['x'], p['y'], 
                                           p['x']+3, p['y']+3)
            
            self.root.after(50, self.animate_particles)
        except:
            pass

    def create_cpu_meter(self):
        """Animated CPU usage meter"""
        meter_frame = tk.Frame(self.header_frame, bg=self.colors["bg"])
        meter_frame.place(relx=0.78, rely=0.2, anchor="nw")
        
        tk.Label(meter_frame, text="💻 CPU LOAD", font=("Segoe UI", 9, "bold"),
                bg=self.colors["bg"], fg=self.colors["text"]).pack()
        
        self.cpu_canvas = tk.Canvas(meter_frame, width=120, height=22, 
                                   highlightthickness=0, bg=self.colors["input_bg"])
        self.cpu_canvas.pack(pady=5)
        
        self.cpu_canvas.create_rectangle(0, 0, 120, 22, outline=self.colors["fg_secondary"])
        self.cpu_bar = self.cpu_canvas.create_rectangle(0, 0, 0, 22, 
                                                        fill=self.colors["green"], 
                                                        outline="")
        
        self.cpu_label = tk.Label(meter_frame, text="0%", 
                                 font=("Segoe UI", 10, "bold"),
                                 bg=self.colors["bg"], fg=self.colors["green"])
        self.cpu_label.pack(pady=2)
        
        self.simulate_cpu_usage()

    def simulate_cpu_usage(self):
        """Simulate CPU meter"""
        try:
            if self.simulation_running:
                usage = random.randint(40, 95)
                color = self.colors["green"] if usage < 60 else self.colors["orange"] if usage < 80 else self.colors["red"]
            else:
                usage = random.randint(5, 25)
                color = self.colors["green"]
            
            self.cpu_canvas.coords(self.cpu_bar, 0, 0, usage * 1.2, 22)
            self.cpu_canvas.itemconfig(self.cpu_bar, fill=color)
            self.cpu_label.config(text=f"{usage}%", fg=color)
            
            self.root.after(1000, self.simulate_cpu_usage)
        except:
            pass

    def show_toast(self, message, icon="✅", color="green", duration=2500):
        """Modern toast notification"""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes('-topmost', True)
        
        screen_width = self.root.winfo_screenwidth()
        toast_width = 350
        toast_x = screen_width - toast_width - 20
        toast.geometry(f"{toast_width}x80+{toast_x}+20")
        
        toast_frame = tk.Frame(toast, bg=self.colors[color], relief="flat", bd=0)
        toast_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        inner_frame = tk.Frame(toast_frame, bg=self.colors["panel"])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        tk.Label(inner_frame, text=icon, font=("Segoe UI", 24), 
                bg=self.colors["panel"], fg=self.colors[color]).pack(side=tk.LEFT, padx=15)
        
        tk.Label(inner_frame, text=message, font=("Segoe UI", 11, "bold"),
                bg=self.colors["panel"], fg=self.colors["text"], wraplength=250).pack(side=tk.LEFT, padx=10)
        
        def fade_out(alpha=1.0):
            if alpha > 0:
                toast.attributes('-alpha', alpha)
                toast.after(50, lambda: fade_out(alpha - 0.05))
            else:
                toast.destroy()
        
        toast.after(duration, fade_out)

    def show_confetti(self):
        """Celebration confetti"""
        confetti_canvas = tk.Canvas(self.root, highlightthickness=0, bg=self.colors["bg"])
        confetti_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        # Lift above all widgets
        try:
            confetti_canvas.tkraise()
        except:
            pass
        
        colors = [self.colors["green"], self.colors["blue"], 
                 self.colors["purple"], self.colors["orange"], self.colors["yellow"]]
        
        particles = []
        for _ in range(80):
            x = random.randint(0, 1200)
            y = random.randint(-100, 0)
            color = random.choice(colors)
            size = random.randint(5, 10)
            
            p = confetti_canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            particles.append({
                'id': p, 'x': x, 'y': y, 
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(3, 8)
            })
        
        def animate_confetti(frame=0):
            if frame < 100:
                for p in particles:
                    p['x'] += p['vx']
                    p['y'] += p['vy']
                    p['vy'] += 0.2
                    
                    try:
                        confetti_canvas.coords(p['id'], p['x'], p['y'], 
                                              p['x']+6, p['y']+6)
                    except:
                        pass
                
                try:
                    confetti_canvas.after(30, lambda: animate_confetti(frame + 1))
                except:
                    pass
            else:
                try:
                    confetti_canvas.destroy()
                except:
                    pass
        
        animate_confetti()

    def bind_keyboard_shortcuts(self):
        """Keyboard shortcuts for quick actions"""
        self.root.bind('<Control-i>', lambda e: self.import_csv())
        self.root.bind('<Control-e>', lambda e: self.export_data())
        self.root.bind('<Control-d>', lambda e: self.clear_all())
        self.root.bind('<Control-r>', lambda e: self.run_simulation())
        self.root.bind('<Control-a>', lambda e: self.ent_pid.focus())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<F5>', lambda e: self.run_simulation())
        self.root.bind('<Delete>', lambda e: self.delete_selected())

    # --- FUNCTIONALITY ---

    def add_process(self):
        """Add process with validation"""
        try:
            pid = self.ent_pid.get().strip()
            arrival = self.ent_arr.get().strip()
            burst = self.ent_burst.get().strip()
            priority = self.ent_priority.get().strip() or "5"
            ptype = self.var_type.get()
            
            if not all([pid, arrival, burst]):
                messagebox.showwarning("Input Error", "Please fill all required fields!")
                return
            
            arrival_int = int(arrival)
            burst_int = int(burst)
            priority_int = int(priority)
            
            if arrival_int < 0 or burst_int <= 0:
                raise ValueError("Times must be positive!")
            
            if not (1 <= priority_int <= 10):
                raise ValueError("Priority must be between 1-10!")
            
            tag = 'foreground' if ptype == 'Foreground' else 'background'
            item = self.tree.insert("", "end", 
                                   values=(pid, arrival, burst, priority, ptype, "Waiting"),
                                   tags=(tag,))
            
            self.process_list.append({
                "pid": pid,
                "arrival": arrival,
                "burst": burst,
                "priority": priority,
                "type": ptype,
                "item_id": item
            })
            
            self.update_statistics()
            
            for entry in [self.ent_pid, self.ent_arr, self.ent_burst, self.ent_priority]:
                entry.delete(0, tk.END)
            self.ent_pid.focus()
            
            self.show_toast(f"Process {pid} added!", "✅", "green")
            self.flash_status("✅ Process added successfully!", "#27ae60")
            
        except ValueError as e:
            self.show_toast(str(e), "❌", "red")
            messagebox.showerror("Invalid Input", str(e))

    def run_simulation(self):
        """Run simulation with animation"""
        if not self.process_list:
            self.show_toast("Add processes first!", "⚠️", "orange")
            messagebox.showerror("Error", "No processes to run!")
            return
        
        if self.simulation_running:
            messagebox.showinfo("Info", "Simulation already running!")
            return
        
        self.simulation_running = True
        self.show_toast("Simulation started!", "▶️", "blue")
        self.flash_status("⚙️ Running simulation...", "#3498db")
        
        self.root.after(100, self.animate_simulation)

    def animate_simulation(self):
        """Animate execution with progress bar"""
        self.gantt_canvas.delete("all")
        
        # Add progress bar at top
        progress_bg = self.gantt_canvas.create_rectangle(50, 20, 600, 35, 
                                                         fill=self.colors["input_bg"], 
                                                         outline=self.colors["fg_secondary"])
        progress_bar = self.gantt_canvas.create_rectangle(50, 20, 50, 35, 
                                                          fill=self.colors["blue"], 
                                                          outline="")
        progress_text = self.gantt_canvas.create_text(325, 27, text="0%", 
                                                     font=("Segoe UI", 10, "bold"),
                                                     fill=self.colors["text"])
        
        x_pos = 50
        y_base = 120
        colors = {"Foreground": "#ff6b6b", "Background": "#4ecdc4"}
        
        sorted_processes = sorted(self.process_list, 
                                 key=lambda p: int(p["arrival"]))
        
        total_energy_standard = 0
        total_energy_dvfs = 0
        total_processes = len(sorted_processes)
        
        for i, process in enumerate(sorted_processes):
            # Update progress bar
            progress_percent = (i + 1) / total_processes
            progress_width = 50 + (550 * progress_percent)
            self.gantt_canvas.coords(progress_bar, 50, 20, progress_width, 35)
            self.gantt_canvas.itemconfig(progress_text, text=f"{int(progress_percent * 100)}%")
            
            burst = int(process["burst"])
            width = burst * 4
            ptype = process["type"]
            color = colors[ptype]
            
            self.gantt_canvas.create_rectangle(
                x_pos, y_base - 30, x_pos + width, y_base + 30,
                fill=color, outline="white", width=2
            )
            
            self.gantt_canvas.create_text(
                x_pos + width//2, y_base,
                text=f"{process['pid']}\n{burst}ms",
                fill="white", font=("Segoe UI", 9, "bold")
            )
            
            self.tree.item(process["item_id"], values=(
                process["pid"], process["arrival"], process["burst"],
                process["priority"], ptype, "Running"
            ))
            self.root.update()
            time.sleep(0.5)
            
            if ptype == "Foreground":
                energy = burst * 1.0
                total_energy_standard += energy
                total_energy_dvfs += energy
            else:
                energy_std = burst * 1.0
                energy_dvfs = burst * 0.6
                total_energy_standard += energy_std
                total_energy_dvfs += energy_dvfs
            
            self.tree.item(process["item_id"], 
                          tags=('completed',),
                          values=(process["pid"], process["arrival"], 
                                 process["burst"], process["priority"], 
                                 ptype, "Completed"))
            
            x_pos += width + 20
            self.root.update()
        
        savings = ((total_energy_standard - total_energy_dvfs) / total_energy_standard * 100) if total_energy_standard > 0 else 0
        
        self.lbl_standard_energy.config(text=f"Standard: {total_energy_standard:.1f} mW")
        self.lbl_dvfs_energy.config(text=f"DVFS: {total_energy_dvfs:.1f} mW")
        self.lbl_savings.config(text=f"💰 Savings: {savings:.1f}%")
        
        self.draw_energy_comparison(total_energy_standard, total_energy_dvfs)
        
        is_efficient = savings > 20
        self.update_battery(is_efficient)
        
        self.stat_cards["⚡ Energy Saved"]['value'].config(text=f"{savings:.1f}%")
        
        self.simulation_running = False
        self.flash_status("✅ Simulation completed!", "#27ae60")
        
        self.show_confetti()
        
        messagebox.showinfo("Success", 
                          f"Simulation Complete!\n\n"
                          f"Standard Energy: {total_energy_standard:.1f} mW\n"
                          f"DVFS Energy: {total_energy_dvfs:.1f} mW\n"
                          f"Savings: {savings:.1f}%")

    def draw_energy_comparison(self, standard, dvfs):
        """Draw bar chart"""
        self.energy_canvas.delete("all")
        
        max_val = max(standard, dvfs) if max(standard, dvfs) > 0 else 1
        scale = 400 / max_val
        
        std_height = standard * scale
        self.energy_canvas.create_rectangle(
            100, 250 - std_height, 180, 250,
            fill="#ff6b6b", outline="white", width=2
        )
        self.energy_canvas.create_text(
            140, 270, text=f"Standard\n{standard:.1f} mW",
            font=("Segoe UI", 9, "bold")
        )
        
        dvfs_height = dvfs * scale
        self.energy_canvas.create_rectangle(
            220, 250 - dvfs_height, 300, 250,
            fill="#27ae60", outline="white", width=2
        )
        self.energy_canvas.create_text(
            260, 270, text=f"DVFS\n{dvfs:.1f} mW",
            font=("Segoe UI", 9, "bold")
        )

    def update_battery(self, is_efficient=True):
        """Update animated ring"""
        if is_efficient:
            level = 90
            color = self.colors["green"]
            status = "⚡ Efficient"
        else:
            level = 60
            color = self.colors["red"]
            status = "⚠️ High Drain"
        
        extent_angle = -(level / 100 * 360)
        self.canvas_batt.itemconfig(self.batt_arc, extent=extent_angle, outline=color)
        self.canvas_batt.itemconfig(self.batt_text, text=f"{level}%", fill=color)
        self.lbl_batt_status.config(text=status, fg=color)

    def update_statistics(self):
        """Update stats"""
        total = len(self.process_list)
        self.stat_cards["📋 Total Tasks"]['value'].config(text=str(total))
        
        if total > 0:
            avg_burst = sum(int(p['burst']) for p in self.process_list) / total
            self.stat_cards["⏱️ Avg Turnaround"]['value'].config(text=f"{avg_burst:.1f} ms")

    def flash_status(self, message, color):
        """Flash status"""
        self.lbl_status.config(text=message, fg=color)
        self.status_dot.itemconfig(self.dot, fill=color)
        self.root.after(3000, lambda: self.lbl_status.config(text="Ready", fg=self.colors["green"]))

    def clear_all(self):
        """Clear all data"""
        if not self.process_list:
            return
        
        if messagebox.askyesno("Confirm", "Clear all processes?"):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.process_list.clear()
            
            self.gantt_canvas.delete("all")
            self.energy_canvas.delete("all")
            
            for card in self.stat_cards.values():
                card['value'].config(text="0")
            
            self.flash_status("🗑️ All data cleared", "#f39c12")

    def search_processes(self, event=None):
        """Search table"""
        query = self.search_entry.get().lower()
        
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if query in str(values).lower():
                self.tree.selection_set(item)
                self.tree.see(item)
                break

    def sort_column(self, col):
        """Sort table"""
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        items.sort()
        
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)

    def show_context_menu(self, event):
        """Context menu"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="🗑️ Delete", command=self.delete_selected)
        menu.add_command(label="✏️ Edit", command=self.edit_selected)
        menu.add_separator()
        menu.add_command(label="❌ Cancel")
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def delete_selected(self):
        """Delete process"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)['values']
            pid = values[0]
            
            self.tree.delete(item)
            self.process_list = [p for p in self.process_list if p['pid'] != pid]
            self.update_statistics()

    def edit_selected(self):
        """Edit process"""
        messagebox.showinfo("Edit", "Edit feature coming soon!")

    def import_csv(self):
        """Import CSV"""
        filename = filedialog.askopenfilename(
            title="Import CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row.get('pid'):
                            self.process_list.append(row)
                            self.tree.insert("", "end", values=(
                                row['pid'], row.get('arrival', '0'), row.get('burst', '0'),
                                row.get('priority', '5'), row.get('type', 'Foreground'), "Waiting"
                            ))
                self.update_statistics()
                messagebox.showinfo("Success", "CSV imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {e}")

    def save_project(self):
        """Save project"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', newline='') as file:
                    writer = csv.DictWriter(file, 
                        fieldnames=['pid', 'arrival', 'burst', 'priority', 'type'])
                    writer.writeheader()
                    writer.writerows(self.process_list)
                messagebox.showinfo("Success", "Project saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")

    def show_statistics(self):
        """Show detailed statistics"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Detailed Statistics")
        stats_window.geometry("500x400")
        stats_window.configure(bg=self.colors["bg"])
        
        stats_text = tk.Text(stats_window, font=("Consolas", 10), wrap=tk.WORD,
                            bg=self.colors["panel"], fg=self.colors["text"])
        stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        total = len(self.process_list)
        if total > 0:
            fg_count = sum(1 for p in self.process_list if p['type'] == 'Foreground')
            bg_count = total - fg_count
            avg_burst = sum(int(p['burst']) for p in self.process_list) / total
            
            stats_text.insert('1.0', f"""
╔════════════════════════════════════════╗
║     DETAILED PROCESS STATISTICS        ║
╚════════════════════════════════════════╝

Total Processes: {total}
├─ Foreground Tasks: {fg_count}
└─ Background Tasks: {bg_count}

Average Burst Time: {avg_burst:.2f} ms
Total Burst Time: {sum(int(p['burst']) for p in self.process_list)} ms

Task Distribution:
├─ High Priority: {fg_count * 100 / total:.1f}%
└─ Low Priority: {bg_count * 100 / total:.1f}%

Energy Optimization:
└─ DVFS Applicable: {"Yes" if bg_count > 0 else "No"}
            """)
        else:
            stats_text.insert('1.0', "No processes available.")

    def show_performance_graph(self):
        """Performance graph"""
        messagebox.showinfo("Graph", "Performance graph feature coming soon!")

    def show_help(self):
        """Help dialog"""
        help_window = tk.Toplevel(self.root)
        help_window.title("User Guide")
        help_window.geometry("600x500")
        help_window.configure(bg=self.colors["bg"])
        
        help_text = tk.Text(help_window, font=("Segoe UI", 10), wrap=tk.WORD,
                           bg=self.colors["panel"], fg=self.colors["text"])
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_text.insert('1.0', """
═══════════════════════════════════════════════
    ENERGY-EFFICIENT SCHEDULER - USER GUIDE
═══════════════════════════════════════════════

🎯 GETTING STARTED:
1. Add processes using the input form
2. Click "RUN SIMULATION" to execute
3. View results in multiple tabs
4. Export reports as CSV

⌨️ KEYBOARD SHORTCUTS:
• Ctrl+I: Import CSV file
• Ctrl+E: Export report
• Ctrl+D: Clear all data
• Ctrl+T: Toggle theme

📊 FEATURES:
• Real-time process visualization
• Gantt chart timeline
• Energy consumption analysis
• DVFS-based power optimization

💡 TIPS:
• Use Background tasks for better energy savings
• Higher priority = More CPU time
• Export reports for analysis

❓ SUPPORT:
For issues, contact Team Abhi
        """)

    def show_about(self):
        """About dialog"""
        messagebox.showinfo("About", 
                          "⚡ CPU ENERGY OPTIMIZER v2.1\n\n"  # Changed version number
                          "DVFS-Based Scheduling System\n"
                          "for Mobile Computing\n\n"
                          "Developed by:\n"
                          "• Abhishek (GUI & Integration)\n"
                          "• Rajeswari (Logic Algorithms)\n"
                          "• Kaushiki (Data Visualization)\n\n"
                          "© 2025 LPU CSE316 Project")

    def export_data(self):
        """Enhanced export"""
        if not self.process_list:
            messagebox.showwarning("No Data", "Nothing to export!")
            return
        
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open("scheduler_report.csv", "w", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                
                writer.writerow(["═" * 80])
                writer.writerow(["ENERGY-EFFICIENT CPU SCHEDULER REPORT"])
                writer.writerow(["Team Abhi - DVFS-Based Scheduling System"])
                writer.writerow(["Generated on:", timestamp])
                writer.writerow(["═" * 80])
                writer.writerow([])
                
                writer.writerow(["Process ID", "Arrival Time (ms)", "Burst Time (ms)", 
                               "Priority", "Task Type", "Power Mode"])
                writer.writerow(["─" * 15] * 6)
                
                for p in self.process_list:
                    power_mode = "High (1.0 GHz)" if p["type"] == "Foreground" else "Low (0.6 GHz)"
                    writer.writerow([
                        p["pid"], p["arrival"], p["burst"], 
                        p.get("priority", "5"), p["type"], power_mode
                    ])
                
                writer.writerow([])
                writer.writerow(["═" * 80])
                writer.writerow(["SUMMARY STATISTICS"])
                writer.writerow(["═" * 80])
                
                total = len(self.process_list)
                total_burst = sum(int(p["burst"]) for p in self.process_list)
                fg_count = sum(1 for p in self.process_list if p["type"] == "Foreground")
                bg_count = total - fg_count
                
                writer.writerow(["Total Processes:", total])
                writer.writerow(["Total Burst Time:", f"{total_burst} ms"])
                writer.writerow(["Foreground Tasks:", fg_count])
                writer.writerow(["Background Tasks:", bg_count])
                writer.writerow(["Energy Mode:", "DVFS Enabled" if bg_count > 0 else "Standard Performance"])
                
                writer.writerow([])
                writer.writerow(["═" * 80])
                writer.writerow(["End of Report"])
                writer.writerow(["═" * 80])
            
            messagebox.showinfo("Success", 
                              "✅ Report exported successfully!\n\n"
                              "File: scheduler_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

    def toggle_theme(self):
        """Toggle theme"""
        self.current_mode = "light" if self.current_mode == "dark" else "dark"
        self.colors = self.themes[self.current_mode]
        self.btn_theme.config(text="🌙 LIGHT" if self.current_mode == "dark" else "☀️ DARK")
        self.apply_theme()

    def apply_theme(self):
        """Apply theme"""
        c = self.colors
        
        self.root.configure(bg=c["bg"])
        self.header_frame.configure(bg=c["bg"])
        self.btn_frame.configure(bg=c["bg"])
        
        self.title_label.configure(bg=c["bg"], fg=c["green"])
        self.subtitle_label.configure(bg=c["bg"], fg=c["fg_secondary"])
        
        self.btn_theme.configure(bg=c["panel"], fg=c["text"])
        
        for card_data in self.stat_cards.values():
            card_data['frame'].configure(bg=c["panel"])
            card_data['title'].configure(bg=c["panel"], fg=c["fg_secondary"])
            card_data['value'].configure(bg=c["panel"], fg=c[card_data['color']])
        
        self.input_frame.configure(bg=c["panel"], highlightbackground=c["green"])
        
        for entry in [self.ent_pid, self.ent_arr, self.ent_burst, self.ent_priority]:
            entry.configure(bg=c["input_bg"], fg=c["text"], 
                          insertbackground=c["text"])
        
        for (btn, color_key) in self.action_buttons.values():
            btn.configure(bg=c[color_key], fg="white")
        
        if hasattr(self, 'batt_frame'):
            self.batt_frame.configure(bg=c["bg"])
            self.canvas_batt.configure(bg=c["bg"])
            self.lbl_batt_status.configure(bg=c["bg"])
        
        if hasattr(self, 'particle_canvas'):
            self.particle_canvas.configure(bg=c["bg"])
        
        if hasattr(self, 'gantt_canvas'):
            self.gantt_canvas.configure(bg=c["panel"])
        
        if hasattr(self, 'energy_canvas'):
            self.energy_canvas.configure(bg=c["panel"])
        
        if hasattr(self, 'status_frame'):
            self.status_frame.configure(bg=c["bg"])
            self.status_dot.configure(bg=c["bg"])
            self.lbl_status.configure(bg=c["bg"], fg=c["text"])
        
        self.style.configure("Treeview", background=c["panel"], 
                           foreground=c["text"], fieldbackground=c["panel"])
        self.style.configure("Treeview.Heading", background=c["bg"], 
                           foreground=c["green"])


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernSchedulerApp(root)
    root.mainloop()
