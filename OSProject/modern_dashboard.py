"""
Energy-Efficient CPU Scheduler - Futuristic Dashboard
Ultra High-End UI using CustomTkinter
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog, Canvas
import threading
import csv
import datetime

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Import team modules
try:
    from logic import Process, schedule_tasks, calculate_energy, get_metrics, convert_to_visualization_format
    from visualization import plot_energy_comparison, draw_gantt_chart
    INTEGRATION_ENABLED = True
    print("✅ Team modules loaded: Rajeswari's Logic + Kaushiki's Visualization")
except ImportError as e:
    INTEGRATION_ENABLED = False
    print(f"⚠️ Running in standalone mode: {e}")


class FuturisticDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Energy-Efficient CPU Scheduler - Futuristic Dashboard")
        self.root.geometry("1550x950")
        
        # Bind cleanup on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Color schemes for dark and light modes
        self.dark_colors = {
            "bg": "#0f1419",
            "panel": "#1e2530",
            "card_bg": "#1a1f2e",
            "text": "#e8ecf5",
            "input_bg": "#3d4556",
            "input_text": "#ffffff",
            "primary": "#00d4ff",
            "primary_hover": "#00b8e6",
            "success": "#00ff88",
            "success_hover": "#00e676",
            "danger": "#ff5370",
            "danger_hover": "#ff3d5c",
            "warning": "#ffaa00",
            "purple": "#b388ff",
            "purple_hover": "#9c6fff",
            "secondary": "#8b92b8",
            "accent": "#00ffa3",
            "glow": "#1a3d4d",
        }
        
        self.light_colors = {
            "bg": "#f0f4f8",
            "panel": "#ffffff",
            "card_bg": "#f8fafc",
            "text": "#0f172a",
            "input_bg": "#e2e8f0",
            "input_text": "#000000",
            "primary": "#0369a1",
            "primary_hover": "#075985",
            "success": "#047857",
            "success_hover": "#065f46",
            "danger": "#dc2626",
            "danger_hover": "#b91c1c",
            "warning": "#d97706",
            "purple": "#7c3aed",
            "purple_hover": "#6d28d9",
            "secondary": "#334155",
            "accent": "#0d9488",
            "glow": "#bae6fd",
        }
        
        self.current_mode = "dark"
        self.colors = self.dark_colors
        
        self.process_list = []
        self.scheduled_processes = None
        self.last_std_energy = 0
        self.last_dvfs_energy = 0
        self.progress_bar = None
        self.progress_label = None
        self.status_blink_id = None
        
        self.create_dashboard()
        self.bind_keyboard_shortcuts()
        self.start_status_blink()
    
    def create_dashboard(self):
        """Create the main futuristic dashboard"""
        # Main scrollable container
        self.main_container = ctk.CTkScrollableFrame(
            self.root,
            fg_color=self.colors['bg'],
            scrollbar_button_color=self.colors['primary'],
            scrollbar_button_hover_color=self.colors['primary_hover']
        )
        self.main_container.pack(fill="both", expand=True)
        
        self.create_top_nav()
        self.create_content_layout()
    
    def bind_keyboard_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Control-a>', lambda e: self.add_process())
        self.root.bind('<Control-r>', lambda e: self.run_simulation())
        self.root.bind('<Control-d>', lambda e: self.clear_all())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<F5>', lambda e: self.run_simulation())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())
    
    def start_status_blink(self):
        """Animate status indicator with pulsing effect"""
        def blink():
            try:
                if hasattr(self, 'status_indicator') and self.status_indicator.winfo_exists():
                    current = self.status_indicator.cget('text')
                    if '●' in current:
                        # Pulse effect by slightly changing opacity
                        self.status_indicator.configure(text=current)
                if hasattr(self, 'root') and self.root.winfo_exists():
                    self.status_blink_id = self.root.after(1000, blink)
            except:
                pass
        blink()
    
    def create_top_nav(self):
        """Create futuristic navigation bar with gradient effect"""
        nav = ctk.CTkFrame(
            self.main_container,
            fg_color=self.colors['primary'],
            corner_radius=0,
            height=110
        )
        nav.pack(fill="x", padx=0, pady=0)
        
        # Add gradient glow effect at bottom
        glow_frame = ctk.CTkFrame(
            nav,
            fg_color=self.colors['glow'],
            corner_radius=0,
            height=4
        )
        glow_frame.pack(side="bottom", fill="x")
        
        # Content container
        nav_content = ctk.CTkFrame(nav, fg_color="transparent")
        nav_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Left: Title
        title_frame = ctk.CTkFrame(nav_content, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="⚡ ENERGY-EFFICIENT CPU SCHEDULER",
            font=("Segoe UI", 26, "bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="FCFS + DVFS Algorithm | Futuristic Dashboard v2.0",
            font=("Segoe UI", 12),
            text_color="#e0f2fe"
        ).pack(anchor="w", pady=(2, 0))
        
        # Right: Action buttons
        btn_frame = ctk.CTkFrame(nav_content, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # Theme toggle button - show opposite theme name
        button_text = "🌙 Dark" if self.current_mode == "light" else "☀️ Light"
        self.theme_toggle_btn = ctk.CTkButton(
            btn_frame,
            text=button_text,
            command=self.toggle_theme,
            fg_color="#1e40af",
            hover_color="#1e3a8a",
            font=("Segoe UI", 13, "bold"),
            width=120,
            height=42,
            corner_radius=12,
            border_width=2,
            border_color="white"
        )
        self.theme_toggle_btn.pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="❓ Help",
            command=self.show_help,
            fg_color=self.colors['purple'],
            hover_color=self.colors['purple_hover'],
            font=("Segoe UI", 13, "bold"),
            width=100,
            height=42,
            corner_radius=12
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Export",
            command=self.export_results,
            fg_color=self.colors['accent'],
            hover_color=self.colors['primary'],
            font=("Segoe UI", 13, "bold"),
            width=110,
            height=42,
            corner_radius=12
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🎨 Sample",
            command=self.load_sample_data,
            fg_color=self.colors['warning'],
            hover_color="#ff9500",
            font=("Segoe UI", 13, "bold"),
            width=110,
            height=42,
            corner_radius=12
        ).pack(side="left", padx=5)
    
    def create_content_layout(self):
        """Create main content layout"""
        content = ctk.CTkFrame(self.main_container, fg_color=self.colors['bg'])
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configure grid
        content.grid_columnconfigure(0, weight=0, minsize=400)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar(content)
        self.create_main_area(content)
    
    def create_sidebar(self, parent):
        """Create futuristic sidebar"""
        sidebar = ctk.CTkFrame(
            parent,
            fg_color=self.colors['panel'],
            corner_radius=15,
            border_width=2,
            border_color=self.colors['primary'],
            width=400
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        sidebar.grid_propagate(False)
        
        # Configure sidebar grid to prevent propagation
        sidebar.grid_rowconfigure(0, weight=0)  # Header row - fixed
        sidebar.grid_rowconfigure(1, weight=1)  # Form row - expandable
        sidebar.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(
            sidebar,
            fg_color=self.colors['primary'],
            corner_radius=12,
            height=75
        )
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        header.grid_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="➕ ADD NEW PROCESS",
            font=("Segoe UI", 20, "bold"),
            text_color="white"
        ).pack(expand=True)
        
        # Scrollable form
        form = ctk.CTkScrollableFrame(
            sidebar,
            fg_color="transparent",
            scrollbar_button_color=self.colors['primary']
        )
        form.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Input fields
        self.entries = {}
        fields = [
            ("PROCESS ID", "pid", "P1"),
            ("ARRIVAL TIME (ms)", "arrival", "0"),
            ("BURST TIME (ms)", "burst", "100"),
            ("PRIORITY", "priority", "1")
        ]
        
        for label, key, placeholder in fields:
            ctk.CTkLabel(
                form,
                text=label,
                font=("Segoe UI", 13, "bold"),
                text_color=self.colors['accent']
            ).pack(anchor="w", pady=(12, 6))
            
            entry = ctk.CTkEntry(
                form,
                placeholder_text=placeholder,
                font=("Segoe UI", 14),
                fg_color=self.colors['input_bg'],
                border_color=self.colors['primary'],
                border_width=2,
                corner_radius=10,
                height=45
            )
            entry.pack(fill="x", pady=(0, 6))
            self.entries[key] = entry
        
        # Task Type - Segmented Button
        ctk.CTkLabel(
            form,
            text="TASK TYPE",
            font=("Segoe UI", 13, "bold"),
            text_color=self.colors['accent']
        ).pack(anchor="w", pady=(20, 10))
        
        self.task_type_var = ctk.StringVar(value="Foreground")
        
        task_segment = ctk.CTkSegmentedButton(
            form,
            values=["Foreground", "Background"],
            variable=self.task_type_var,
            fg_color=self.colors['input_bg'],
            selected_color=self.colors['primary'],
            selected_hover_color=self.colors['primary_hover'],
            unselected_color=self.colors['card_bg'],
            unselected_hover_color=self.colors['panel'],
            font=("Segoe UI", 13, "bold"),
            corner_radius=10,
            border_width=2,
            height=45
        )
        task_segment.pack(fill="x", pady=(0, 20))
        
        # Action Buttons
        ctk.CTkButton(
            form,
            text="✓ ADD PROCESS",
            command=self.add_process,
            fg_color=self.colors['purple'],
            hover_color=self.colors['purple_hover'],
            font=("Segoe UI", 15, "bold"),
            height=50,
            corner_radius=12,
            border_width=2,
            border_color=self.colors['accent']
        ).pack(fill="x", pady=6)
        
        ctk.CTkButton(
            form,
            text="▶️ RUN SIMULATION",
            command=self.run_simulation,
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            font=("Segoe UI", 14, "bold"),
            height=45,
            corner_radius=12
        ).pack(fill="x", pady=6)
        
        ctk.CTkButton(
            form,
            text="🗑️ CLEAR ALL",
            command=self.clear_all,
            fg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            font=("Segoe UI", 13, "bold"),
            height=42,
            corner_radius=12
        ).pack(fill="x", pady=6)
        
        # Divider
        ctk.CTkFrame(form, fg_color=self.colors['primary'], height=3).pack(fill="x", pady=20)
        
        # Quick Actions
        ctk.CTkLabel(
            form,
            text="⚡ QUICK ACTIONS",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['accent']
        ).pack(anchor="w", pady=(0, 12))
        
        actions = [
            ("📊 Gantt Chart", self.show_gantt_chart, self.colors['purple']),
            ("⚡ Energy Chart", self.show_energy_chart, self.colors['warning']),
            ("💾 Save CSV", self.save_to_csv, self.colors['secondary'])
        ]
        
        for text, cmd, color in actions:
            ctk.CTkButton(
                form,
                text=text,
                command=cmd,
                fg_color=color,
                hover_color=self.colors['panel'],
                font=("Segoe UI", 12, "bold"),
                height=38,
                corner_radius=10
            ).pack(fill="x", pady=4)
        
        # Divider
        ctk.CTkFrame(form, fg_color=self.colors['primary'], height=3).pack(fill="x", pady=20)
        
        # Statistics
        ctk.CTkLabel(
            form,
            text="📊 STATISTICS",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['accent']
        ).pack(anchor="w", pady=(0, 12))
        
        self.stat_labels = {}
        stats = [
            ("Total Processes", "total", self.colors['primary']),
            ("Foreground Tasks", "fg", self.colors['danger']),
            ("Background Tasks", "bg", self.colors['success'])
        ]
        
        for label, key, color in stats:
            stat_card = ctk.CTkFrame(
                form,
                fg_color=self.colors['card_bg'],
                corner_radius=12,
                border_width=2,
                border_color=color
            )
            stat_card.pack(fill="x", pady=6)
            
            content_frame = ctk.CTkFrame(stat_card, fg_color="transparent")
            content_frame.pack(fill="x", padx=18, pady=14)
            
            ctk.CTkLabel(
                content_frame,
                text=label,
                font=("Segoe UI", 11, "bold"),
                text_color=self.colors['secondary']
            ).pack(side="left")
            
            value_label = ctk.CTkLabel(
                content_frame,
                text="0",
                font=("Segoe UI", 22, "bold"),
                text_color=color
            )
            value_label.pack(side="right")
            self.stat_labels[key] = value_label
    
    def create_main_area(self, parent):
        """Create main content area"""
        main = ctk.CTkFrame(parent, fg_color=self.colors['bg'])
        main.grid(row=0, column=1, sticky="nsew")
        
        # Configure grid
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
        
        self.create_process_queue(main)
        self.create_charts_row(main)
    
    def create_process_queue(self, parent):
        """Create process queue section"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['panel'],
            corner_radius=15,
            border_width=2,
            border_color=self.colors['accent']
        )
        card.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        
        # Header
        header_frame = ctk.CTkFrame(card, fg_color=self.colors['purple'], corner_radius=12)
        header_frame.pack(fill="x", padx=15, pady=15)
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="x", padx=20, pady=16)
        
        ctk.CTkLabel(
            header_content,
            text="📋 PROCESS QUEUE",
            font=("Segoe UI", 22, "bold"),
            text_color="white"
        ).pack(side="left")
        
        ctk.CTkButton(
            header_content,
            text="🗑️ Remove Selected",
            command=self.remove_selected,
            fg_color=self.colors['danger'],
            hover_color=self.colors['danger_hover'],
            font=("Segoe UI", 12, "bold"),
            width=160,
            height=36,
            corner_radius=10
        ).pack(side="right")
        
        # Table display
        table_frame = ctk.CTkFrame(
            card,
            fg_color=self.colors['card_bg'],
            corner_radius=12
        )
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.process_textbox = ctk.CTkTextbox(
            table_frame,
            font=("Consolas", 12),
            fg_color=self.colors['input_bg'],
            corner_radius=10,
            border_width=2,
            border_color=self.colors['primary'],
            height=220,
            wrap="none"
        )
        self.process_textbox.pack(fill="both", expand=True, padx=12, pady=12)
        
        # Disable backspace and delete keys to prevent manual editing
        self.process_textbox.bind("<BackSpace>", lambda e: "break")
        self.process_textbox.bind("<Delete>", lambda e: "break")
        self.process_textbox.bind("<Key>", lambda e: "break" if e.keysym not in ["Up", "Down", "Left", "Right", "Home", "End", "Prior", "Next"] else None)
        
        self.update_process_display()
    
    def create_charts_row(self, parent):
        """Create charts row with Gantt and Energy"""
        charts_container = ctk.CTkFrame(parent, fg_color=self.colors['bg'])
        charts_container.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        
        charts_container.grid_columnconfigure(0, weight=1)
        charts_container.grid_columnconfigure(1, weight=1)
        charts_container.grid_rowconfigure(0, weight=1)
        
        self.create_gantt_chart(charts_container)
        self.create_energy_analysis(charts_container)
    
    def create_gantt_chart(self, parent):
        """Create Gantt chart section"""
        # Outer shadow frame
        shadow_frame = ctk.CTkFrame(
            parent,
            fg_color="#0a1929",
            corner_radius=18
        )
        shadow_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        
        card = ctk.CTkFrame(
            shadow_frame,
            fg_color="#0d1b2a",
            corner_radius=15,
            border_width=3,
            border_color="#1e3a8a"
        )
        card.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Header with gradient effect
        header = ctk.CTkFrame(card, fg_color="#1e3a8a", corner_radius=12, height=70)
        header.pack(fill="x", padx=15, pady=15)
        header.pack_propagate(False)
        
        # Glow line at top
        glow_top = ctk.CTkFrame(header, fg_color="#60a5fa", corner_radius=0, height=3)
        glow_top.pack(side="top", fill="x")
        
        ctk.CTkLabel(
            header,
            text="📊 PROCESS EXECUTION TIMELINE",
            font=("Segoe UI", 20, "bold"),
            text_color="#e0f2fe"
        ).pack(expand=True)
        
        # Canvas container with horizontal scrollbar
        canvas_frame = ctk.CTkFrame(card, fg_color="#0f172a", corner_radius=12, border_width=2, border_color="#1e40af")
        canvas_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Create horizontal scrollbar
        h_scrollbar = ctk.CTkScrollbar(
            canvas_frame,
            orientation="horizontal",
            button_color="#3b82f6",
            button_hover_color="#60a5fa"
        )
        h_scrollbar.pack(side="bottom", fill="x", padx=12, pady=(0, 12))
        
        self.gantt_canvas = Canvas(
            canvas_frame,
            bg="#1e293b",
            height=320,
            highlightthickness=0,
            xscrollcommand=h_scrollbar.set
        )
        self.gantt_canvas.pack(fill="both", expand=True, padx=12, pady=(12, 0))
        
        # Configure scrollbar to control canvas
        h_scrollbar.configure(command=self.gantt_canvas.xview)
        
        self.gantt_text_id = self.gantt_canvas.create_text(
            350, 160,
            text="⏳ Run simulation to see the timeline",
            font=("Segoe UI", 16, "bold"),
            fill="#64748b"
        )
    
    def create_energy_analysis(self, parent):
        """Create energy analysis section"""
        # Outer shadow frame
        shadow_frame = ctk.CTkFrame(
            parent,
            fg_color="#0a1929",
            corner_radius=18
        )
        shadow_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        
        card = ctk.CTkFrame(
            shadow_frame,
            fg_color="#0d1b2a",
            corner_radius=15,
            border_width=3,
            border_color="#1e3a8a"
        )
        card.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Header with gradient effect
        header = ctk.CTkFrame(card, fg_color="#1e3a8a", corner_radius=12, height=70)
        header.pack(fill="x", padx=15, pady=15)
        header.pack_propagate(False)
        
        # Glow line at top
        glow_top = ctk.CTkFrame(header, fg_color="#60a5fa", corner_radius=0, height=3)
        glow_top.pack(side="top", fill="x")
        
        ctk.CTkLabel(
            header,
            text="⚡ ENERGY CONSUMPTION ANALYSIS",
            font=("Segoe UI", 20, "bold"),
            text_color="#e0f2fe"
        ).pack(expand=True)
        
        # Canvas container
        canvas_frame = ctk.CTkFrame(card, fg_color="#0f172a", corner_radius=12, border_width=2, border_color="#1e40af")
        canvas_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.energy_canvas = Canvas(
            canvas_frame,
            bg="#1e293b",
            height=240,
            highlightthickness=0
        )
        self.energy_canvas.pack(fill="x", padx=12, pady=12)
        
        # Metrics
        metrics_container = ctk.CTkFrame(canvas_frame, fg_color="transparent")
        metrics_container.pack(fill="x", padx=12, pady=(0, 12))
        
        self.metric_cards = {}
        metrics = [
            ("Standard Energy", "std", "#ef4444", "mW"),
            ("DVFS Energy", "dvfs", "#06b6d4", "mW"),
            ("Savings", "savings", "#3b82f6", "%")
        ]
        
        for label, key, color, unit in metrics:
            # Outer glow frame for each metric
            glow_frame = ctk.CTkFrame(
                metrics_container,
                fg_color="#0a1929",
                corner_radius=12
            )
            glow_frame.pack(fill="x", pady=5)
            
            metric_card = ctk.CTkFrame(
                glow_frame,
                fg_color="#1e293b",
                corner_radius=10,
                border_width=2,
                border_color=color
            )
            metric_card.pack(fill="both", expand=True, padx=2, pady=2)
            
            content = ctk.CTkFrame(metric_card, fg_color="transparent")
            content.pack(fill="x", padx=18, pady=14)
            
            ctk.CTkLabel(
                content,
                text=label,
                font=("Segoe UI", 12, "bold"),
                text_color="#94a3b8"
            ).pack(side="left")
            
            value_label = ctk.CTkLabel(
                content,
                text=f"0 {unit}",
                font=("Segoe UI", 22, "bold"),
                text_color=color
            )
            value_label.pack(side="right")
            
            self.metric_cards[key] = (value_label, unit)
    
    def update_process_display(self):
        """Update process queue display"""
        self.process_textbox.delete("1.0", "end")
        
        # Header
        header = f"{'PID':<12} {'Arrival':<12} {'Burst':<12} {'Priority':<12} {'Type':<15} {'Status':<20}\n"
        separator = "=" * 95 + "\n"
        
        self.process_textbox.insert("end", header, "header")
        self.process_textbox.insert("end", separator, "separator")
        
        # Data rows
        if not self.process_list:
            self.process_textbox.insert("end", "\n" + " " * 25 + "No processes added yet...\n", "empty")
        else:
            for p in self.process_list:
                status = p.get('status', '⏳ Ready')
                row = f"{p['pid']:<12} {p['arrival']:<12} {p['burst']:<12} {p['priority']:<12} {p['type']:<15} {status:<20}\n"
                self.process_textbox.insert("end", row)
        
        # Styling (without font as CTkTextbox doesn't support it in tag_config)
        self.process_textbox.tag_config("header", foreground=self.colors['accent'])
        self.process_textbox.tag_config("separator", foreground=self.colors['primary'])
        self.process_textbox.tag_config("empty", foreground=self.colors['secondary'])
    
    def update_stats(self):
        """Update statistics with animation"""
        total = len(self.process_list)
        fg = sum(1 for p in self.process_list if p['type'] == 'Foreground')
        bg = total - fg
        
        self.animate_stat_change(self.stat_labels['total'], str(total))
        self.animate_stat_change(self.stat_labels['fg'], str(fg))
        self.animate_stat_change(self.stat_labels['bg'], str(bg))
    
    def animate_stat_change(self, label, new_value):
        """Animate stat value change with counting effect"""
        try:
            old_value = int(label.cget('text'))
            new_val = int(new_value)
            
            if old_value == new_val:
                return
            
            steps = min(abs(new_val - old_value), 10)
            if steps == 0:
                label.configure(text=new_value)
                return
            
            increment = (new_val - old_value) / steps
            
            def update_step(current, step):
                if step <= steps:
                    label.configure(text=str(int(current)))
                    self.root.after(30, lambda: update_step(current + increment, step + 1))
                else:
                    label.configure(text=new_value)
            
            update_step(old_value, 1)
        except:
            label.configure(text=new_value)
    
    def add_process(self):
        """Add process to queue"""
        try:
            pid = self.entries['pid'].get().strip() or f"P{len(self.process_list)+1}"
            arrival = int(self.entries['arrival'].get() or "0")
            burst = int(self.entries['burst'].get() or "100")
            priority = int(self.entries['priority'].get() or "1")
            task_type = self.task_type_var.get()
            
            # Validate inputs
            if burst <= 0:
                messagebox.showerror("Error", "Burst time must be positive!")
                return
            
            if arrival < 0:
                messagebox.showerror("Error", "Arrival time cannot be negative!")
                return
            
            if priority < 1:
                messagebox.showerror("Error", "Priority must be at least 1!")
                return
            
            self.process_list.append({
                'pid': pid,
                'arrival': arrival,
                'burst': burst,
                'priority': priority,
                'type': task_type,
                'status': '⏳ Ready'
            })
            
            for entry in self.entries.values():
                entry.delete(0, "end")
            
            self.update_process_display()
            self.update_stats()
            self.show_toast(f"✓ Process {pid} added!", self.colors['success'])
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")
    
    def remove_selected(self):
        """Remove selected process"""
        if not self.process_list:
            messagebox.showwarning("No Processes", "No processes to remove!")
            return
        
        if self.process_list:
            removed = self.process_list.pop()
            self.update_process_display()
            self.update_stats()
            self.show_toast(f"✓ Process {removed['pid']} removed!", self.colors['warning'])
    
    def clear_all(self):
        """Clear all processes"""
        if not self.process_list:
            return
        
        if messagebox.askyesno("Confirm", "Clear all processes?"):
            self.process_list.clear()
            self.scheduled_processes = None
            
            # Reset energy values
            self.last_std_energy = 0
            self.last_dvfs_energy = 0
            
            # Clear Gantt chart
            self.gantt_canvas.delete('all')
            self.gantt_text_id = self.gantt_canvas.create_text(
                350, 160,
                text="⏳ Run simulation to see the timeline",
                font=("Segoe UI", 15),
                fill=self.colors['secondary']
            )
            
            # Clear energy canvas
            self.energy_canvas.delete('all')
            
            # Reset metrics display
            self.metric_cards['std'][0].configure(text="0 mW")
            self.metric_cards['dvfs'][0].configure(text="0 mW")
            self.metric_cards['savings'][0].configure(text="0 %")
            
            self.update_process_display()
            self.update_stats()
            self.show_toast("✓ All cleared!", self.colors['danger'])
    
    def load_sample_data(self):
        """Load sample processes for demo"""
        sample_processes = [
            {"pid": "P1", "arrival": 0, "burst": 100, "priority": 1, "type": "Foreground"},
            {"pid": "P2", "arrival": 50, "burst": 150, "priority": 2, "type": "Background"},
            {"pid": "P3", "arrival": 100, "burst": 80, "priority": 3, "type": "Background"},
            {"pid": "P4", "arrival": 150, "burst": 120, "priority": 1, "type": "Foreground"},
        ]
        
        self.process_list.clear()
        self.scheduled_processes = None
        self.last_std_energy = 0
        self.last_dvfs_energy = 0
        
        for p in sample_processes:
            p['status'] = '⏳ Ready'
            self.process_list.append(p)
        
        # Clear visualizations
        self.gantt_canvas.delete('all')
        self.gantt_text_id = self.gantt_canvas.create_text(
            350, 160,
            text="⏳ Run simulation to see the timeline",
            font=("Segoe UI", 15),
            fill=self.colors['secondary']
        )
        self.energy_canvas.delete('all')
        
        # Reset metrics
        self.metric_cards['std'][0].configure(text="0 mW")
        self.metric_cards['dvfs'][0].configure(text="0 mW")
        self.metric_cards['savings'][0].configure(text="0 %")
        
        self.update_process_display()
        self.update_stats()
        self.show_toast("✓ Sample data loaded! Click RUN to test.", self.colors['primary'])
    
    def run_simulation(self):
        """Run scheduling simulation with animated progress"""
        if not self.process_list:
            messagebox.showwarning("No Processes", "Please add processes first!")
            return
        
        if not INTEGRATION_ENABLED:
            messagebox.showerror("Error", "Logic module not available!")
            return
        
        try:
            self.update_status("RUNNING", self.colors['warning'])
            self.show_progress_bar()
            self.show_toast("⏳ Running simulation...", self.colors['warning'])
            
            processes = [
                Process(p['pid'], p['arrival'], p['burst'], p['type'])
                for p in self.process_list
            ]
            
            self.scheduled_processes = schedule_tasks(processes)
            self.last_std_energy, self.last_dvfs_energy = calculate_energy(self.scheduled_processes)
            savings = ((self.last_std_energy - self.last_dvfs_energy) / self.last_std_energy * 100) if self.last_std_energy > 0 else 0
            
            metrics = get_metrics(self.scheduled_processes)
            
            # Update visuals
            self.draw_gantt_inline()
            self.draw_energy_bars()
            
            # Update metrics
            self.metric_cards['std'][0].configure(text=f"{self.last_std_energy:.1f} mW")
            self.metric_cards['dvfs'][0].configure(text=f"{self.last_dvfs_energy:.1f} mW")
            self.metric_cards['savings'][0].configure(text=f"{savings:.1f} %")
            
            # Update statuses
            for p in self.scheduled_processes:
                for p_data in self.process_list:
                    if p_data['pid'] == p.pid:
                        p_data['status'] = f"✓ Done ({p.completion_time:.1f}ms)"
                        break
            
            self.update_process_display()
            self.update_status("COMPLETE", self.colors['success'])
            
            self.hide_progress_bar()
            self.show_toast(f"✓ Complete! Energy saved: {savings:.1f}%", self.colors['success'])
            
            messagebox.showinfo("Simulation Complete",
                              f"✅ Scheduling Successful!\n\n"
                              f"⚡ Energy Savings: {savings:.1f}%\n"
                              f"⏱️ Avg Turnaround: {metrics['avg_turnaround']:.1f}ms\n"
                              f"⏳ Avg Waiting: {metrics['avg_waiting']:.1f}ms\n"
                              f"⚡ Avg Response: {metrics['avg_response']:.1f}ms")
            
        except Exception as e:
            self.hide_progress_bar()
            self.update_status("ERROR", self.colors['danger'])
            messagebox.showerror("Error", f"Simulation failed:\n{str(e)}")
    
    def draw_gantt_inline(self):
        """Draw Gantt chart with correct execution timeline"""
        self.gantt_canvas.delete('all')
        
        if not self.scheduled_processes:
            return
        
        self.gantt_canvas.update_idletasks()
        canvas_width = max(self.gantt_canvas.winfo_width(), 700)
        
        x_start = 50
        y_start = 40
        bar_height = 45
        
        max_time = max(p.completion_time for p in self.scheduled_processes)
        scale = (canvas_width - 100) / max_time if max_time > 0 else 1
        
        # Enhanced color scheme for bars
        colors = {
            'Foreground': '#3b82f6',  # Bright blue
            'Background': '#06b6d4'   # Cyan
        }
        
        for i, p in enumerate(self.scheduled_processes):
            y = y_start + (i * (bar_height + 12))
            
            # Calculate actual start time (when process started executing)
            start_time = p.completion_time - p.burst_time
            end_time = p.completion_time
            
            start_x = x_start + (start_time * scale)
            width = p.burst_time * scale
            
            color = colors.get(p.task_type, '#64748b')
            
            # Shadow for 3D effect
            self.gantt_canvas.create_rectangle(
                start_x + 3, y + 3, start_x + width + 3, y + bar_height + 3,
                fill='#0f172a', outline='', width=0
            )
            
            # Execution bar with gradient effect
            self.gantt_canvas.create_rectangle(
                start_x, y, start_x + width, y + bar_height,
                fill=color, outline='#60a5fa', width=2
            )
            
            # Inner highlight for depth
            self.gantt_canvas.create_rectangle(
                start_x + 4, y + 4, start_x + width - 4, y + bar_height - 4,
                fill='', outline='#93c5fd', width=1
            )
            
            # Process label with shadow
            self.gantt_canvas.create_text(
                start_x + width/2 + 1, y + bar_height/2 + 1,
                text=f"{p.pid}\n{p.burst_time:.0f}ms",
                fill='#0f172a', font=('Segoe UI', 11, 'bold')
            )
            self.gantt_canvas.create_text(
                start_x + width/2, y + bar_height/2,
                text=f"{p.pid}\n{p.burst_time:.0f}ms",
                fill='#e0f2fe', font=('Segoe UI', 11, 'bold')
            )
            
            # Start time marker
            self.gantt_canvas.create_text(
                start_x, y + bar_height + 18,
                text=f"{start_time:.0f}",
                fill='#60a5fa', font=('Segoe UI', 10, 'bold')
            )
            
            # End time marker
            self.gantt_canvas.create_text(
                start_x + width, y + bar_height + 18,
                text=f"{end_time:.0f}",
                fill='#94a3b8', font=('Segoe UI', 10)
            )
            
            # Show arrival time with dashed line if there's waiting time
            arrival_x = x_start + (p.arrival_time * scale)
            if arrival_x < start_x - 10:  # Only show if there's visible gap
                self.gantt_canvas.create_line(
                    arrival_x, y + bar_height/2, start_x - 5, y + bar_height/2,
                    fill='#f59e0b', width=2, arrow='last', dash=(4, 2)
                )
                self.gantt_canvas.create_text(
                    arrival_x, y - 10,
                    text=f"⏰{p.arrival_time:.0f}",
                    fill='#fbbf24', font=('Segoe UI', 9, 'bold')
                )
    
    def draw_energy_bars(self):
        """Draw energy bars"""
        self.energy_canvas.delete('all')
        
        self.energy_canvas.update_idletasks()
        canvas_width = max(self.energy_canvas.winfo_width(), 700)
        
        max_val = max(self.last_std_energy, self.last_dvfs_energy) if max(self.last_std_energy, self.last_dvfs_energy) > 0 else 1
        scale = 180 / max_val
        
        # Standard Energy Bar
        std_height = self.last_std_energy * scale
        x1 = canvas_width/2 - 130
        y_base = 220
        
        # Shadow for Standard bar
        self.energy_canvas.create_rectangle(
            x1 + 4, y_base - std_height + 4, x1 + 94, y_base + 4,
            fill='#0f172a', outline='', width=0
        )
        
        # Standard bar with gradient effect
        self.energy_canvas.create_rectangle(
            x1, y_base - std_height, x1 + 90, y_base,
            fill='#ef4444', outline='#f87171', width=3
        )
        
        # Inner highlight
        self.energy_canvas.create_rectangle(
            x1 + 5, y_base - std_height + 5, x1 + 85, y_base - 5,
            fill='', outline='#fca5a5', width=1
        )
        
        self.energy_canvas.create_text(
            x1 + 45, y_base - std_height - 18,
            text=f"{self.last_std_energy:.1f}mW",
            fill='#fca5a5', font=('Segoe UI', 13, 'bold')
        )
        self.energy_canvas.create_text(
            x1 + 45, y_base + 18,
            text="Standard",
            fill='#e0f2fe', font=('Segoe UI', 12, 'bold')
        )
        
        # DVFS Energy Bar
        dvfs_height = self.last_dvfs_energy * scale
        x2 = canvas_width/2 + 40
        
        # Shadow for DVFS bar
        self.energy_canvas.create_rectangle(
            x2 + 4, y_base - dvfs_height + 4, x2 + 94, y_base + 4,
            fill='#0f172a', outline='', width=0
        )
        
        # DVFS bar with gradient effect
        self.energy_canvas.create_rectangle(
            x2, y_base - dvfs_height, x2 + 90, y_base,
            fill='#06b6d4', outline='#22d3ee', width=3
        )
        
        # Inner highlight
        self.energy_canvas.create_rectangle(
            x2 + 5, y_base - dvfs_height + 5, x2 + 85, y_base - 5,
            fill='', outline='#67e8f9', width=1
        )
        
        self.energy_canvas.create_text(
            x2 + 45, y_base - dvfs_height - 18,
            text=f"{self.last_dvfs_energy:.1f}mW",
            fill='#67e8f9', font=('Segoe UI', 13, 'bold')
        )
        self.energy_canvas.create_text(
            x2 + 45, y_base + 18,
            text="DVFS",
            fill='#e0f2fe', font=('Segoe UI', 12, 'bold')
        )
    
    def show_gantt_chart(self):
        """Show full Gantt chart"""
        if not self.scheduled_processes:
            messagebox.showwarning("No Data", "Run simulation first!")
            return
        
        try:
            gantt_data = convert_to_visualization_format(self.scheduled_processes)
            threading.Thread(target=lambda: draw_gantt_chart(gantt_data), daemon=True).start()
            self.show_toast("📊 Opening chart...", self.colors['primary'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed:\n{str(e)}")
    
    def show_energy_chart(self):
        """Show full energy chart"""
        if self.last_std_energy == 0:
            messagebox.showwarning("No Data", "Run simulation first!")
            return
        
        try:
            threading.Thread(
                target=lambda: plot_energy_comparison(self.last_std_energy, self.last_dvfs_energy),
                daemon=True
            ).start()
            self.show_toast("⚡ Opening chart...", self.colors['primary'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed:\n{str(e)}")
    
    def save_to_csv(self):
        """Save to CSV with beautiful formatting"""
        if not self.process_list:
            messagebox.showwarning("No Data", "No processes to save!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=f"scheduler_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Beautiful header section
                    writer.writerow(['⚡ Energy-Efficient CPU Scheduler - Process Data'])
                    writer.writerow(['Generated:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow(['Algorithm:', 'FCFS + DVFS'])
                    writer.writerow(['Total Processes:', len(self.process_list)])
                    writer.writerow([])
                    
                    # Column headers with emojis
                    writer.writerow(['🆔 Process ID', '⏰ Arrival (ms)', '⚡ Burst (ms)', '🎯 Priority', '📌 Task Type', '📊 Status'])
                    writer.writerow(['=' * 15, '=' * 15, '=' * 15, '=' * 15, '=' * 15, '=' * 25])
                    
                    # Data rows
                    for p in self.process_list:
                        status = p.get('status', '⏳ Ready')
                        writer.writerow([p['pid'], p['arrival'], p['burst'], p['priority'], p['type'], status])
                    
                    writer.writerow([])
                    writer.writerow(['━' * 80])
                    writer.writerow(['✅ Export completed successfully!'])
                
                self.show_toast("✓ CSV Saved with beautiful formatting!", self.colors['success'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed:\n{str(e)}")
    
    def export_results(self):
        """Export results with beautiful formatting"""
        if not self.scheduled_processes:
            messagebox.showwarning("No Data", "Run simulation first!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                initialfile=f"results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if filename:
                savings = ((self.last_std_energy - self.last_dvfs_energy) / self.last_std_energy * 100) if self.last_std_energy > 0 else 0
                metrics = get_metrics(self.scheduled_processes)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    # Beautiful header with ASCII art
                    f.write("\n")
                    f.write("╔" + "═" * 78 + "╗\n")
                    f.write("║" + " " * 15 + "⚡ ENERGY-EFFICIENT CPU SCHEDULER ⚡" + " " * 15 + "║\n")
                    f.write("║" + " " * 20 + "Simulation Results Report" + " " * 21 + "║\n")
                    f.write("╚" + "═" * 78 + "╝\n\n")
                    
                    # Metadata section
                    f.write("┌─ 📋 REPORT INFORMATION " + "─" * 52 + "\n")
                    f.write(f"│ 📅 Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"│ 🔧 Algorithm: FCFS + DVFS (Dynamic Voltage Frequency Scaling)\n")
                    f.write(f"│ 📊 Total Processes: {len(self.scheduled_processes)}\n")
                    f.write(f"│ 👥 Team: Abhishek (GUI) | Rajeswari (Logic) | Kaushiki (Visualization)\n")
                    f.write("└" + "─" * 77 + "\n\n")
                    
                    # Process details section
                    f.write("┌─ 🔄 PROCESS EXECUTION DETAILS " + "─" * 45 + "\n│\n")
                    
                    for i, p in enumerate(self.scheduled_processes, 1):
                        f.write(f"│ ╔═══ Process {i}/{len(self.scheduled_processes)}: {p.pid} {'═' * (55 - len(p.pid))}\n")
                        f.write(f"│ ║ 🆔 Process ID        : {p.pid}\n")
                        f.write(f"│ ║ ⏰ Arrival Time      : {p.arrival_time:.2f} ms\n")
                        f.write(f"│ ║ ⚡ Burst Time        : {p.burst_time:.2f} ms\n")
                        f.write(f"│ ║ 📌 Task Type         : {p.task_type}\n")
                        f.write(f"│ ║ ✅ Completion Time   : {p.completion_time:.2f} ms\n")
                        f.write(f"│ ║ 🔄 Turnaround Time   : {p.turnaround_time:.2f} ms\n")
                        f.write(f"│ ║ ⏳ Waiting Time      : {p.waiting_time:.2f} ms\n")
                        f.write(f"│ ║ ⚙️  Response Time     : {p.response_time:.2f} ms\n")
                        f.write(f"│ ║ ⚡ Energy Consumed   : {p.energy_consumed:.2f} mW\n")
                        f.write(f"│ ╚" + "═" * 69 + "\n│\n")
                    
                    f.write("└" + "─" * 77 + "\n\n")
                    
                    # Energy analysis with visual bars
                    f.write("┌─ ⚡ ENERGY CONSUMPTION ANALYSIS " + "─" * 43 + "\n│\n")
                    f.write(f"│ 🔴 Standard Energy (No DVFS)  : {self.last_std_energy:.2f} mW\n")
                    f.write(f"│ {'█' * int(self.last_std_energy / 10)}\n│\n")
                    f.write(f"│ 🟢 DVFS Optimized Energy      : {self.last_dvfs_energy:.2f} mW\n")
                    f.write(f"│ {'█' * int(self.last_dvfs_energy / 10)}\n│\n")
                    f.write(f"│ 💰 Energy Savings             : {savings:.2f}%\n")
                    f.write(f"│ 📉 Energy Reduced             : {self.last_std_energy - self.last_dvfs_energy:.2f} mW\n│\n")
                    f.write("└" + "─" * 77 + "\n\n")
                    
                    # Performance metrics
                    f.write("┌─ 📈 PERFORMANCE METRICS " + "─" * 51 + "\n│\n")
                    f.write(f"│ ⏱️  Average Turnaround Time   : {metrics['avg_turnaround']:.2f} ms\n")
                    f.write(f"│ ⏳ Average Waiting Time       : {metrics['avg_waiting']:.2f} ms\n")
                    f.write(f"│ ⚡ Average Response Time      : {metrics['avg_response']:.2f} ms\n")
                    f.write(f"│ 🎯 CPU Utilization           : {(sum(p.burst_time for p in self.scheduled_processes) / max(p.completion_time for p in self.scheduled_processes) * 100):.2f}%\n│\n")
                    f.write("└" + "─" * 77 + "\n\n")
                    
                    # Summary section
                    f.write("╔" + "═" * 78 + "╗\n")
                    f.write("║" + " " * 28 + "📊 SUMMARY" + " " * 28 + "║\n")
                    f.write("╠" + "═" * 78 + "╣\n")
                    f.write("║ ✅ Simulation completed successfully!" + " " * 40 + "║\n")
                    f.write(f"║ 💡 DVFS algorithm achieved {savings:.1f}% energy savings" + " " * (26 - len(f"{savings:.1f}")) + "║\n")
                    f.write(f"║ 🚀 Processed {len(self.scheduled_processes)} tasks efficiently with optimal energy usage" + " " * (20 - len(str(len(self.scheduled_processes)))) + "║\n")
                    f.write("╚" + "═" * 78 + "╝\n\n")
                    
                    f.write("" + "─" * 80 + "\n")
                    f.write("Generated by Energy-Efficient CPU Scheduler v2.0\n")
                    f.write("Futuristic Dashboard | © 2024 Team Project\n")
                    f.write("" + "─" * 80 + "\n")
                
                self.show_toast("✓ Beautiful report exported!", self.colors['success'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed:\n{str(e)}")
    
    def toggle_theme(self):
        """Toggle theme"""
        # Switch mode
        if self.current_mode == "dark":
            self.current_mode = "light"
            self.colors = self.light_colors
            ctk.set_appearance_mode("light")
        else:
            self.current_mode = "dark"
            self.colors = self.dark_colors
            ctk.set_appearance_mode("dark")
        
        # Store current data
        stored_processes = self.process_list.copy()
        stored_scheduled = self.scheduled_processes
        stored_std = self.last_std_energy
        stored_dvfs = self.last_dvfs_energy
        
        # Recreate dashboard
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        self.create_top_nav()
        self.create_content_layout()
        
        # Restore data
        self.process_list = stored_processes
        self.scheduled_processes = stored_scheduled
        self.last_std_energy = stored_std
        self.last_dvfs_energy = stored_dvfs
        
        self.update_process_display()
        self.update_stats()
        
        # Redraw if simulation was run
        if self.scheduled_processes:
            self.draw_gantt_inline()
            self.draw_energy_bars()
            savings = ((self.last_std_energy - self.last_dvfs_energy) / self.last_std_energy * 100) if self.last_std_energy > 0 else 0
            self.metric_cards['std'][0].configure(text=f"{self.last_std_energy:.1f} mW")
            self.metric_cards['dvfs'][0].configure(text=f"{self.last_dvfs_energy:.1f} mW")
            self.metric_cards['savings'][0].configure(text=f"{savings:.1f} %")
        
        self.show_toast(f"✓ Switched to {self.current_mode.title()} mode!", self.colors['primary'])
    
    def show_help(self):
        """Show help"""
        help_text = """
⚡ Energy-Efficient CPU Scheduler - Help

🎯 Features:
• FCFS + DVFS Algorithm
• Real-time visualization
• All content visible
• Futuristic UI with CustomTkinter

⌨️ Shortcuts:
• Ctrl+A - Add Process
• Ctrl+R / F5 - Run
• Ctrl+D - Clear
• F1 - Help

📊 Usage:
1. Enter process details
2. Select task type
3. Click Add Process
4. Run Simulation
5. View results!

💾 Export:
• CSV for process data
• Text for results

👥 Team:
• Abhishek - GUI
• Rajeswari - Logic
• Kaushiki - Visualization
"""
        messagebox.showinfo("Help", help_text)
    
    def show_progress_bar(self):
        """Show animated progress bar during simulation"""
        # Create progress window
        self.progress_window = ctk.CTkToplevel(self.root)
        self.progress_window.title("Processing...")
        self.progress_window.geometry("400x150")
        self.progress_window.transient(self.root)
        self.progress_window.grab_set()
        
        # Center the window
        self.progress_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 200
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 75
        self.progress_window.geometry(f"+{x}+{y}")
        
        # Content
        ctk.CTkLabel(
            self.progress_window,
            text="⚡ Running Simulation",
            font=("Segoe UI", 18, "bold"),
            text_color=self.colors['primary']
        ).pack(pady=20)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_window,
            text="Initializing...",
            font=("Segoe UI", 12)
        )
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_window,
            width=350,
            height=20,
            corner_radius=10,
            progress_color=self.colors['primary']
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)
        
        # Animate progress
        self.animate_progress()
    
    def animate_progress(self, value=0):
        """Animate progress bar"""
        if hasattr(self, 'progress_bar') and self.progress_bar.winfo_exists():
            if value < 1.0:
                self.progress_bar.set(value)
                
                # Update label
                if value < 0.3:
                    self.progress_label.configure(text="Scheduling processes...")
                elif value < 0.6:
                    self.progress_label.configure(text="Calculating energy consumption...")
                elif value < 0.9:
                    self.progress_label.configure(text="Generating visualizations...")
                else:
                    self.progress_label.configure(text="Finalizing results...")
                
                self.root.after(50, lambda: self.animate_progress(value + 0.02))
    
    def hide_progress_bar(self):
        """Hide progress bar"""
        if hasattr(self, 'progress_window'):
            try:
                if self.progress_window and self.progress_window.winfo_exists():
                    self.progress_window.destroy()
                    self.progress_window = None
            except:
                pass
    
    def update_status(self, status, color):
        """Update status indicator with animation"""
        if hasattr(self, 'status_indicator'):
            status_text = f"● {status}"
            self.status_indicator.configure(text=status_text, text_color=color)
    
    def show_toast(self, message, color):
        """Show enhanced toast notification"""
        toast = ctk.CTkToplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes('-topmost', True)
        
        # Shadow frame
        shadow = ctk.CTkFrame(toast, fg_color=self.colors['glow'], corner_radius=12)
        shadow.pack(padx=3, pady=3)
        
        # Main frame
        frame = ctk.CTkFrame(shadow, fg_color=color, corner_radius=10, border_width=2, border_color="white")
        frame.pack()
        
        ctk.CTkLabel(
            frame,
            text=message,
            font=("Segoe UI", 13, "bold"),
            text_color="white"
        ).pack(padx=30, pady=18)
        
        toast.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (toast.winfo_width() // 2)
        y = self.root.winfo_y() + self.root.winfo_height() - 100
        toast.geometry(f"+{x}+{y}")
        
        toast.after(2000, toast.destroy)
    
    def on_closing(self):
        """Cleanup when closing window"""
        try:
            # Cancel any pending after callbacks
            if hasattr(self, 'status_blink_id') and self.status_blink_id:
                self.root.after_cancel(self.status_blink_id)
            
            # Close progress window if open
            if hasattr(self, 'progress_window') and self.progress_window:
                try:
                    self.progress_window.destroy()
                except:
                    pass
        except:
            pass
        finally:
            self.root.destroy()


def main():
    print("\n" + "="*60)
    print("⚡ Energy-Efficient CPU Scheduler")
    print("Futuristic Dashboard with CustomTkinter")
    print("="*60)
    print("\n🚀 Starting application...\n")
    
    root = ctk.CTk()
    app = FuturisticDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
