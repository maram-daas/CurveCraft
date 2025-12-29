import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import CubicSpline
from scipy.signal import savgol_filter
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class CurveAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("CurveCraft - Parametric Expression Analyzer")
        self.root.configure(bg='#fffdf0')
        self.root.geometry("1400x900")
        
        # State
        self.raw_points = []
        self.drawing = False
        self.parametric_curve = None
        self.fourier_curve = None
        self.is_closed = False
        self.harmonics = 15
        self.show_mode = 'parametric'
        self.x_range = 1.2  # Default x range
        self.y_range = 1.2  # Default y range
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#ffd700', height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_frame = tk.Frame(header, bg='#ffd700')
        title_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(title_frame, text="CurveCraft", font=('Helvetica', 32, 'bold'), 
                bg='#ffd700', fg='#333333').pack()
        
        tk.Label(title_frame, text="Draw curves and extract mathematical expressions", 
                font=('Helvetica', 14), bg='#ffd700', fg='#666666').pack(pady=(5, 0))
        
        # Main content area
        content = tk.Frame(self.root, bg='#fffdf0')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Left side - Drawing canvas
        left_panel = tk.Frame(content, bg='#ffffff', highlightbackground='#ffd700', 
                             highlightthickness=3, width=500, relief=tk.RAISED)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 25))
        left_panel.pack_propagate(False)
        
        canvas_header = tk.Frame(left_panel, bg='#fff8e1', height=70)
        canvas_header.pack(fill=tk.X)
        canvas_header.pack_propagate(False)
        
        tk.Label(canvas_header, text="Drawing Canvas", font=('Helvetica', 16, 'bold'),
                bg='#fff8e1', fg='#b8860b').pack(side=tk.LEFT, padx=25, pady=15)
        
        btn_frame = tk.Frame(canvas_header, bg='#fff8e1')
        btn_frame.pack(side=tk.RIGHT, padx=25)
        
        reset_btn = tk.Button(btn_frame, text="Clear Canvas", command=self.reset,
                             bg='#ff6b6b', fg='white', font=('Helvetica', 11, 'bold'),
                             relief=tk.FLAT, bd=0, padx=25, pady=8, cursor='hand2',
                             activebackground='#ff5252', activeforeground='white',
                             width=15)
        reset_btn.pack()
        
        # Drawing instructions
        instructions = tk.Frame(left_panel, bg='#fffdf0', height=30)
        instructions.pack(fill=tk.X, pady=(10, 5))
        tk.Label(instructions, text="Click and drag to draw | Double-click to complete", 
                bg='#fffdf0', fg='#666666', font=('Helvetica', 10, 'italic')).pack()
        
        # Custom range controls
        range_frame = tk.Frame(left_panel, bg='#fffdf0', height=60)
        range_frame.pack(fill=tk.X, pady=(5, 10))
        
        # X-axis range
        x_range_frame = tk.Frame(range_frame, bg='#fffdf0')
        x_range_frame.pack(fill=tk.X, padx=25, pady=2)
        
        tk.Label(x_range_frame, text="X Range:", bg='#fffdf0', fg='#666666',
                font=('Helvetica', 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        # Current x-range display
        self.x_range_label = tk.Label(x_range_frame, text=f"±{self.x_range:.1f}", 
                                     bg='#fffdf0', fg='#333333', font=('Helvetica', 10, 'bold'))
        self.x_range_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # X-range entry
        self.x_range_entry = tk.Entry(x_range_frame, width=8, font=('Helvetica', 10),
                                     bd=2, relief=tk.SOLID, justify='center')
        self.x_range_entry.insert(0, "1.2")
        self.x_range_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        x_set_btn = tk.Button(x_range_frame, text="Set", command=self.set_x_range,
                             bg='#ffd700', fg='#333333', font=('Helvetica', 9),
                             width=4, relief=tk.FLAT, cursor='hand2',
                             activebackground='#ffc800', padx=5, pady=2)
        x_set_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Y-axis range
        y_range_frame = tk.Frame(range_frame, bg='#fffdf0')
        y_range_frame.pack(fill=tk.X, padx=25, pady=2)
        
        tk.Label(y_range_frame, text="Y Range:", bg='#fffdf0', fg='#666666',
                font=('Helvetica', 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        # Current y-range display
        self.y_range_label = tk.Label(y_range_frame, text=f"±{self.y_range:.1f}", 
                                     bg='#fffdf0', fg='#333333', font=('Helvetica', 10, 'bold'))
        self.y_range_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Y-range entry
        self.y_range_entry = tk.Entry(y_range_frame, width=8, font=('Helvetica', 10),
                                     bd=2, relief=tk.SOLID, justify='center')
        self.y_range_entry.insert(0, "1.2")
        self.y_range_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        y_set_btn = tk.Button(y_range_frame, text="Set", command=self.set_y_range,
                             bg='#ffd700', fg='#333333', font=('Helvetica', 9),
                             width=4, relief=tk.FLAT, cursor='hand2',
                             activebackground='#ffc800', padx=5, pady=2)
        y_set_btn.pack(side=tk.LEFT)
        
        # Preset ranges
        preset_frame = tk.Frame(range_frame, bg='#fffdf0')
        preset_frame.pack(fill=tk.X, padx=25, pady=(5, 0))
        
        tk.Label(preset_frame, text="Presets:", bg='#fffdf0', fg='#666666',
                font=('Helvetica', 9)).pack(side=tk.LEFT, padx=(0, 5))
        
        for label, (x_val, y_val) in [("1x1", (1.0, 1.0)), ("2x2", (2.0, 2.0)), 
                                      ("πxπ", (3.14, 3.14)), ("10x10", (10.0, 10.0))]:
            btn = tk.Button(preset_frame, text=label, 
                           command=lambda x=x_val, y=y_val: self.set_both_ranges(x, y),
                           bg='#e0f7fa', fg='#006064', font=('Helvetica', 9),
                           width=4, relief=tk.FLAT, cursor='hand2',
                           activebackground='#b2ebf2', padx=2, pady=1)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Matplotlib canvas
        self.fig, self.ax = plt.subplots(figsize=(5, 5), facecolor='#ffffff')
        self.setup_canvas()
        
        canvas_frame = tk.Frame(left_panel, bg='#ffffff')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.canvas = FigureCanvasTkAgg(self.fig, canvas_frame)
        self.canvas.get_tk_widget().configure(bg='#ffffff', highlightthickness=0)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('button_press_event', self.on_double_click)
        
        # Status
        status_frame = tk.Frame(left_panel, bg='#fff8e1', height=50)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Click and drag to draw your curve", 
                                     bg='#fff8e1', fg='#d4a017', font=('Helvetica', 12))
        self.status_label.pack(pady=12)
        
        # Right side - Equations display
        right_panel = tk.Frame(content, bg='#ffffff', highlightbackground='#ffd700',
                              highlightthickness=3, relief=tk.RAISED)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        eq_header = tk.Frame(right_panel, bg='#fff8e1')
        eq_header.pack(fill=tk.X, padx=25, pady=20)
        
        tk.Label(eq_header, text="Mathematical Expressions", font=('Helvetica', 18, 'bold'),
                bg='#fff8e1', fg='#b8860b').pack(side=tk.LEFT)
        
        export_btn = tk.Button(eq_header, text="Copy All", command=self.copy_equations,
                              bg='#ffd700', fg='#333333', font=('Helvetica', 11, 'bold'),
                              relief=tk.FLAT, bd=0, padx=25, pady=10, cursor='hand2',
                              activebackground='#ffc800', activeforeground='#333333',
                              width=12)
        export_btn.pack(side=tk.RIGHT)
        
        # Mode selector
        mode_frame = tk.Frame(right_panel, bg='#ffffff')
        mode_frame.pack(fill=tk.X, padx=25, pady=(0, 15))
        
        tk.Label(mode_frame, text="Display Mode:", bg='#ffffff', fg='#666666',
                font=('Helvetica', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 15))
        
        self.mode_var = tk.StringVar(value='parametric')
        
        param_radio = tk.Radiobutton(mode_frame, text="Parametric (Piecewise)", 
                                     variable=self.mode_var, value='parametric',
                                     command=self.change_mode, bg='#ffffff', fg='#333333',
                                     selectcolor='#ffffff', font=('Helvetica', 11, 'bold'),
                                     activebackground='#ffffff', activeforeground='#333333')
        param_radio.pack(side=tk.LEFT, padx=(0, 25))
        
        self.fourier_radio = tk.Radiobutton(mode_frame, text="Fourier Series", 
                                            variable=self.mode_var, value='fourier',
                                            command=self.change_mode, bg='#ffffff', fg='#666666',
                                            selectcolor='#ffffff', font=('Helvetica', 11),
                                            activebackground='#ffffff', activeforeground='#666666',
                                            state='disabled')
        self.fourier_radio.pack(side=tk.LEFT)
        
        # Main equations text area
        text_container = tk.Frame(right_panel, bg='#ffffff')
        text_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 10))
        
        # Create a frame with scrollbar for equations
        eq_frame = tk.Frame(text_container, bg='#ffffff')
        eq_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        eq_scrollbar = ttk.Scrollbar(eq_frame)
        eq_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget for equations
        self.equations_text = tk.Text(eq_frame, wrap=tk.WORD, bg='#ffffff', fg='#333333',
                                     font=('Consolas', 11), bd=0, insertbackground='#ffd700',
                                     selectbackground='#ffd700', selectforeground='#333333',
                                     padx=20, pady=20, yscrollcommand=eq_scrollbar.set,
                                     height=8)
        self.equations_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        eq_scrollbar.config(command=self.equations_text.yview)
        
        # Configure text tags
        self.equations_text.tag_configure('title', foreground='#b8860b', font=('Helvetica', 20, 'bold'))
        self.equations_text.tag_configure('header', foreground='#d4a017', font=('Helvetica', 14, 'bold'))
        self.equations_text.tag_configure('equation', foreground='#1e88e5', font=('Consolas', 12, 'bold'))
        self.equations_text.tag_configure('coefficient', foreground='#e53935', font=('Consolas', 11))
        self.equations_text.tag_configure('info', foreground='#666666', font=('Helvetica', 11))
        self.equations_text.tag_configure('highlight', foreground='#ff6b00', font=('Helvetica', 11, 'bold'))
        self.equations_text.tag_configure('segment', foreground='#43a047', font=('Consolas', 10))
        
        # Frame for Fourier coefficients table
        self.coeff_container = tk.Frame(right_panel, bg='#ffffff')
        
        # Compact Fourier controls
        self.controls = tk.Frame(right_panel, bg='#fff8e1', highlightbackground='#ffd700',
                                highlightthickness=2, relief=tk.RAISED, height=100)
        
        ctrl_inner = tk.Frame(self.controls, bg='#fff8e1')
        ctrl_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)
        
        control_row1 = tk.Frame(ctrl_inner, bg='#fff8e1')
        control_row1.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(control_row1, text="Fourier Harmonics:", bg='#fff8e1', 
                fg='#b8860b', font=('Helvetica', 11, 'bold')).pack(side=tk.LEFT)
        
        self.harmonics_var = tk.IntVar(value=15)
        harmonics_entry = tk.Entry(control_row1, textvariable=self.harmonics_var, 
                                  width=6, font=('Helvetica', 11), justify='center',
                                  bd=2, relief=tk.SOLID)
        harmonics_entry.pack(side=tk.LEFT, padx=(10, 20))
        harmonics_entry.bind('<Return>', lambda e: self.update_harmonics_from_entry())
        
        self.harmonics_scale = ttk.Scale(control_row1, from_=3, to=50, orient=tk.HORIZONTAL,
                                        variable=self.harmonics_var, 
                                        command=lambda v: self.update_harmonics(float(v)),
                                        length=200)
        self.harmonics_scale.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        control_row2 = tk.Frame(ctrl_inner, bg='#fff8e1')
        control_row2.pack(fill=tk.X)
        
        tk.Label(control_row2, text="Quick set:", bg='#fff8e1', fg='#666666',
                font=('Helvetica', 10)).pack(side=tk.LEFT)
        
        for n in [5, 10, 15, 25, 35]:
            btn = tk.Button(control_row2, text=f"{n}", command=lambda x=n: self.set_harmonics(x),
                           bg='#ffd700', fg='#333333', font=('Helvetica', 9),
                           width=3, relief=tk.FLAT, cursor='hand2',
                           activebackground='#ffc800', padx=2, pady=1)
            btn.pack(side=tk.LEFT, padx=3)
        
        self.controls.pack_forget()
        self.coeff_container.pack_forget()
        
        self.show_initial_message()
    
    def set_x_range(self):
        try:
            value = float(self.x_range_entry.get())
            if value <= 0:
                raise ValueError("Range must be positive")
            self.x_range = value
            self.x_range_label.config(text=f"±{value:.2f}")
            self.setup_canvas()
            if self.parametric_curve is not None:
                self.render_curve()
            else:
                self.canvas.draw_idle()
            self.status_label.config(text=f"X-range set to ±{value:.2f}", fg='#1e88e5')
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please enter a positive number for X range")
    
    def set_y_range(self):
        try:
            value = float(self.y_range_entry.get())
            if value <= 0:
                raise ValueError("Range must be positive")
            self.y_range = value
            self.y_range_label.config(text=f"±{value:.2f}")
            self.setup_canvas()
            if self.parametric_curve is not None:
                self.render_curve()
            else:
                self.canvas.draw_idle()
            self.status_label.config(text=f"Y-range set to ±{value:.2f}", fg='#1e88e5')
        except ValueError as e:
            messagebox.showerror("Invalid Input", "Please enter a positive number for Y range")
    
    def set_both_ranges(self, x_val, y_val):
        self.x_range = x_val
        self.y_range = y_val
        self.x_range_entry.delete(0, tk.END)
        self.x_range_entry.insert(0, str(x_val))
        self.y_range_entry.delete(0, tk.END)
        self.y_range_entry.insert(0, str(y_val))
        self.x_range_label.config(text=f"±{x_val:.2f}")
        self.y_range_label.config(text=f"±{y_val:.2f}")
        self.setup_canvas()
        if self.parametric_curve is not None:
            self.render_curve()
        else:
            self.canvas.draw_idle()
        self.status_label.config(text=f"Range set to X:±{x_val:.2f}, Y:±{y_val:.2f}", fg='#1e88e5')
    
    def setup_canvas(self):
        """Setup or reset the canvas with axes and grid"""
        self.ax.clear()
        self.ax.set_facecolor('#ffffff')
        
        # Set limits based on custom ranges
        self.ax.set_xlim(-self.x_range, self.x_range)
        self.ax.set_ylim(-self.y_range, self.y_range)
        self.ax.set_aspect('equal')
        
        # Calculate grid spacing (approximately 10 squares across)
        x_grid_spacing = self.x_range / 5
        y_grid_spacing = self.y_range / 5
        
        # Set ticks
        x_ticks = []
        current = -self.x_range
        while current <= self.x_range:
            if abs(current) > 0.01 * self.x_range:  # Don't show 0 twice
                x_ticks.append(round(current, 2))
            current += x_grid_spacing
        
        y_ticks = []
        current = -self.y_range
        while current <= self.y_range:
            if abs(current) > 0.01 * self.y_range:  # Don't show 0 twice
                y_ticks.append(round(current, 2))
            current += y_grid_spacing
        
        self.ax.set_xticks(x_ticks)
        self.ax.set_yticks(y_ticks)
        
        # Format tick labels to show fewer decimals
        self.ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}' if abs(x) < 10 else f'{x:.0f}'))
        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, p: f'{y:.1f}' if abs(y) < 10 else f'{y:.0f}'))
        
        # Add faint axis lines at x=0 and y=0
        self.ax.axhline(y=0, color='#cccccc', linewidth=0.8, alpha=0.7, linestyle='-', zorder=0)
        self.ax.axvline(x=0, color='#cccccc', linewidth=0.8, alpha=0.7, linestyle='-', zorder=0)
        
        # Add axis labels
        self.ax.set_xlabel('x', fontsize=12, fontweight='bold', color='#b8860b')
        self.ax.set_ylabel('y', fontsize=12, fontweight='bold', color='#b8860b')
        
        # Grid - lighter and more subtle
        self.ax.grid(True, alpha=0.15, color='#ffd700', linewidth=0.5, linestyle='-', zorder=0)
        
        # Major grid lines for integer values
        major_x_ticks = np.arange(-np.ceil(self.x_range), np.ceil(self.x_range) + 1)
        major_y_ticks = np.arange(-np.ceil(self.y_range), np.ceil(self.y_range) + 1)
        
        for tick in major_x_ticks:
            if -self.x_range <= tick <= self.x_range:
                self.ax.axvline(x=tick, color='#ffd700', linewidth=0.3, alpha=0.2, linestyle='-', zorder=0)
        
        for tick in major_y_ticks:
            if -self.y_range <= tick <= self.y_range:
                self.ax.axhline(y=tick, color='#ffd700', linewidth=0.3, alpha=0.2, linestyle='-', zorder=0)
        
        # Border
        for spine in self.ax.spines.values():
            spine.set_color('#ffd700')
            spine.set_linewidth(3)
        
        # Add info about grid spacing in title
        grid_info = f"Grid: x∈[{-self.x_range:.1f},{self.x_range:.1f}], y∈[{-self.y_range:.1f},{self.y_range:.1f}]"
        self.ax.set_title(grid_info, fontsize=10, color='#666666', pad=10)
    
    def create_coefficients_table(self):
        """Create a larger scrollable table for Fourier coefficients"""
        for widget in self.coeff_container.winfo_children():
            widget.destroy()
        
        if self.fourier_curve is None:
            return
        
        harmonics = self.harmonics_var.get()
        x_fft = self.fourier_curve['x_fft']
        y_fft = self.fourier_curve['y_fft']
        n = self.fourier_curve['n']
        
        header_frame = tk.Frame(self.coeff_container, bg='#ffffff')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(header_frame, text="Fourier Coefficients Table", 
                font=('Helvetica', 16, 'bold'), bg='#ffffff', fg='#b8860b').pack(anchor='w')
        
        table_frame = tk.Frame(self.coeff_container, bg='#ffffff')
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        canvas = tk.Canvas(table_frame, bg='#ffffff', highlightthickness=0, height=300)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        headers = ["k", "aₖ (x cos)", "bₖ (x sin)", "cₖ (y cos)", "dₖ (y sin)"]
        for col, header in enumerate(headers):
            header_label = tk.Label(scrollable_frame, text=header, 
                                  font=('Helvetica', 11, 'bold'),
                                  bg='#fff8e1', fg='#b8860b',
                                  padx=15, pady=8, relief=tk.RAISED, bd=1)
            header_label.grid(row=0, column=col, sticky='ew', padx=1, pady=1)
        
        for k in range(harmonics + 1):
            if k == 0:
                a0_x = np.real(x_fft[0]) / n
                a0_y = np.real(y_fft[0]) / n
                values = [f"{k}", f"{a0_x:.8f}", "0.00000000", f"{a0_y:.8f}", "0.00000000"]
            else:
                an = 2 * np.real(x_fft[k]) / n
                bn = -2 * np.imag(x_fft[k]) / n
                cn = 2 * np.real(y_fft[k]) / n
                dn = -2 * np.imag(y_fft[k]) / n
                values = [f"{k}", f"{an:.8f}", f"{bn:.8f}", f"{cn:.8f}", f"{dn:.8f}"]
            
            bg_color = '#ffffff' if k % 2 == 0 else '#fff8e1'
            
            for col, value in enumerate(values):
                cell = tk.Label(scrollable_frame, text=value, 
                              font=('Consolas', 10),
                              bg=bg_color, fg='#333333',
                              padx=15, pady=6, relief=tk.SUNKEN, bd=1)
                cell.grid(row=k+1, column=col, sticky='ew', padx=1, pady=1)
        
        for col in range(5):
            scrollable_frame.grid_columnconfigure(col, weight=1)
    
    def set_harmonics(self, n):
        self.harmonics_var.set(n)
        self.update_harmonics(n)
    
    def update_harmonics_from_entry(self):
        try:
            n = self.harmonics_var.get()
            if n < 3:
                n = 3
                self.harmonics_var.set(3)
            elif n > 50:
                n = 50
                self.harmonics_var.set(50)
            self.update_harmonics(n)
        except:
            self.harmonics_var.set(15)
            self.update_harmonics(15)
    
    def on_double_click(self, event):
        if event.dblclick and self.drawing:
            self.drawing = False
            self.process_stroke()
    
    def show_initial_message(self):
        self.equations_text.config(state='normal')
        self.equations_text.delete('1.0', tk.END)
        
        self.equations_text.insert('1.0', "Welcome to CurveCraft\n\n", 'title')
        self.equations_text.insert(tk.END, "Draw any shape on the canvas and watch it transform into mathematical expressions.\n\n", 'info')
        
        self.equations_text.insert(tk.END, "What You'll Get:\n\n", 'header')
        self.equations_text.insert(tk.END, "  • Parametric equations: ", 'info')
        self.equations_text.insert(tk.END, "x(t)", 'equation')
        self.equations_text.insert(tk.END, " and ", 'info')
        self.equations_text.insert(tk.END, "y(t)\n", 'equation')
        self.equations_text.insert(tk.END, "  • Cubic polynomial coefficients for each segment\n", 'info')
        self.equations_text.insert(tk.END, "  • Fourier series approximation (for closed curves)\n", 'info')
        self.equations_text.insert(tk.END, "  • Interactive harmonic control\n", 'info')
        self.equations_text.insert(tk.END, "  • Scrollable Fourier coefficients table\n\n", 'info')
        
        self.equations_text.insert(tk.END, "Quick Start:\n\n", 'header')
        self.equations_text.insert(tk.END, "1. ", 'highlight')
        self.equations_text.insert(tk.END, "Set X and Y ranges above the canvas\n", 'info')
        self.equations_text.insert(tk.END, "2. ", 'highlight')
        self.equations_text.insert(tk.END, "Draw a shape on the canvas\n", 'info')
        self.equations_text.insert(tk.END, "3. ", 'highlight')
        self.equations_text.insert(tk.END, "View parametric equations automatically\n", 'info')
        self.equations_text.insert(tk.END, "4. ", 'highlight')
        self.equations_text.insert(tk.END, "For closed curves, switch to Fourier mode\n", 'info')
        
        self.equations_text.insert(tk.END, "Tips:\n\n", 'header')
        self.equations_text.insert(tk.END, "  • Use presets or enter custom ranges\n", 'highlight')
        self.equations_text.insert(tk.END, "  • Each square represents 0.2 units (default)\n", 'highlight')
        self.equations_text.insert(tk.END, "  • Draw slowly for smoother curves\n", 'highlight')
        self.equations_text.insert(tk.END, "  • Close your shape for Fourier analysis\n", 'highlight')
        
        self.equations_text.config(state='disabled')
    
    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.drawing = True
        self.raw_points = [(event.xdata, event.ydata)]
        
    def on_motion(self, event):
        if not self.drawing or event.inaxes != self.ax:
            return
        if len(self.raw_points) > 0 and event.xdata and event.ydata:
            last = self.raw_points[-1]
            dist = np.sqrt((event.xdata - last[0])**2 + (event.ydata - last[1])**2)
            if dist > 0.01 * min(self.x_range, self.y_range):
                self.raw_points.append((event.xdata, event.ydata))
                self.render_drawing()
        
    def on_release(self, event):
        if not self.drawing:
            return
        self.drawing = False
        
        if len(self.raw_points) < 5:
            messagebox.showwarning("Too Short", "Draw a longer curve! Try making a complete shape.")
            self.reset()
            return
            
        self.process_stroke()
        
    def render_drawing(self):
        if len(self.raw_points) < 2:
            return
        points = np.array(self.raw_points)
        for line in self.ax.lines[:]:
            if line.get_label() == '_drawing':
                line.remove()
        self.ax.plot(points[:, 0], points[:, 1], color='#ff9800', 
                    linewidth=4, alpha=0.9, label='_drawing')
        self.canvas.draw_idle()
        
    def smooth_points(self, points):
        if len(points) < 10:
            return points
        points = np.array(points)
        try:
            window = min(11, len(points) if len(points) % 2 == 1 else len(points) - 1)
            x_smooth = savgol_filter(points[:, 0], window_length=window, polyorder=3)
            y_smooth = savgol_filter(points[:, 1], window_length=window, polyorder=3)
            smoothed = np.column_stack([x_smooth, y_smooth])
            step = max(1, len(smoothed) // 25)
            return smoothed[::step]
        except:
            return points[::max(1, len(points) // 25)]
    
    def process_stroke(self):
        smoothed = self.smooth_points(self.raw_points)
        
        # Check if closed - scale threshold by range
        first, last = smoothed[0], smoothed[-1]
        x_threshold = 0.1 * self.x_range
        y_threshold = 0.1 * self.y_range
        x_close = abs(first[0] - last[0]) < x_threshold
        y_close = abs(first[1] - last[1]) < y_threshold
        self.is_closed = x_close and y_close
        
        # Arc-length parameterization
        distances = np.sqrt(np.sum(np.diff(smoothed, axis=0)**2, axis=1))
        cumulative = np.concatenate([[0], np.cumsum(distances)])
        total = cumulative[-1]
        t = cumulative / total if total > 0 else np.linspace(0, 1, len(smoothed))
        
        x, y = smoothed[:, 0], smoothed[:, 1]
        self.x_spline = CubicSpline(t, x, bc_type='natural')
        self.y_spline = CubicSpline(t, y, bc_type='natural')
        
        self.parametric_curve = {'t': t, 'x': x, 'y': y}
        
        if self.is_closed:
            self.compute_fourier()
            self.status_label.config(text=f"Closed curve detected | {len(t)} control points | Fourier available", fg='#43a047')
            self.fourier_radio.config(state='normal', fg='#333333')
        else:
            self.fourier_curve = None
            self.status_label.config(text=f"Open curve | {len(t)} control points", fg='#1e88e5')
            self.fourier_radio.config(state='disabled', fg='#cccccc')
            self.mode_var.set('parametric')
            self.show_mode = 'parametric'
            self.controls.pack_forget()
            self.coeff_container.pack_forget()
        
        self.update_equations_display()
        self.render_curve()
    
    def compute_fourier(self):
        n = 256
        t_sample = np.linspace(0, 1, n, endpoint=False)
        x_sample = self.x_spline(t_sample)
        y_sample = self.y_spline(t_sample)
        
        self.fourier_curve = {
            'x_fft': np.fft.fft(x_sample),
            'y_fft': np.fft.fft(y_sample),
            'n': n
        }
    
    def get_spline_polynomial(self, spline, segment_idx):
        c = spline.c[:, segment_idx]
        return c
    
    def update_equations_display(self):
        self.equations_text.config(state='normal')
        self.equations_text.delete('1.0', tk.END)
        
        if self.parametric_curve is None:
            self.show_initial_message()
            return
        
        if self.show_mode == 'parametric':
            self.equations_text.insert('1.0', "PARAMETRIC EQUATIONS\n\n", 'title')
            
            t = self.parametric_curve['t']
            n_segments = len(t) - 1
            
            self.equations_text.insert(tk.END, f"Curve defined by {n_segments} piecewise cubic polynomial segments:\n\n", 'info')
            
            self.equations_text.insert(tk.END, "GENERAL FORM\n", 'header')
            self.equations_text.insert(tk.END, "-" * 80 + "\n\n", 'info')
            
            for seg_idx in range(n_segments):
                t0 = t[seg_idx]
                t1 = t[seg_idx + 1]
                
                x_coeffs = self.get_spline_polynomial(self.x_spline, seg_idx)
                y_coeffs = self.get_spline_polynomial(self.y_spline, seg_idx)
                
                self.equations_text.insert(tk.END, f"Segment {seg_idx + 1}: ", 'header')
                self.equations_text.insert(tk.END, f"t ∈ [{t0:.4f}, {t1:.4f}]\n", 'segment')
                
                self.equations_text.insert(tk.END, "  x(t) = ", 'equation')
                dt_str = f"(t - {t0:.4f})"
                
                terms = []
                if abs(x_coeffs[0]) > 1e-10:
                    terms.append(f"{x_coeffs[0]:.6f}·{dt_str}³")
                if abs(x_coeffs[1]) > 1e-10:
                    terms.append(f"{x_coeffs[1]:+.6f}·{dt_str}²")
                if abs(x_coeffs[2]) > 1e-10:
                    terms.append(f"{x_coeffs[2]:+.6f}·{dt_str}")
                if abs(x_coeffs[3]) > 1e-10 or len(terms) == 0:
                    terms.append(f"{x_coeffs[3]:+.6f}")
                
                self.equations_text.insert(tk.END, " ".join(terms) + "\n", 'coefficient')
                
                self.equations_text.insert(tk.END, "  y(t) = ", 'equation')
                
                terms = []
                if abs(y_coeffs[0]) > 1e-10:
                    terms.append(f"{y_coeffs[0]:.6f}·{dt_str}³")
                if abs(y_coeffs[1]) > 1e-10:
                    terms.append(f"{y_coeffs[1]:+.6f}·{dt_str}²")
                if abs(y_coeffs[2]) > 1e-10:
                    terms.append(f"{y_coeffs[2]:+.6f}·{dt_str}")
                if abs(y_coeffs[3]) > 1e-10 or len(terms) == 0:
                    terms.append(f"{y_coeffs[3]:+.6f}")
                
                self.equations_text.insert(tk.END, " ".join(terms) + "\n\n", 'coefficient')
            
            self.equations_text.insert(tk.END, "=" * 80 + "\n\n", 'info')
            self.equations_text.insert(tk.END, "Summary\n", 'header')
            self.equations_text.insert(tk.END, f"  • Total segments: {n_segments}\n", 'info')
            self.equations_text.insert(tk.END, f"  • Parameter range: t ∈ [0, 1]\n", 'info')
            self.equations_text.insert(tk.END, f"  • Curve type: {'Closed loop' if self.is_closed else 'Open path'}\n", 'info')
            
            if self.is_closed:
                self.equations_text.insert(tk.END, "\nTip: ", 'highlight')
                self.equations_text.insert(tk.END, "Switch to Fourier mode for a continuous expression with detailed coefficients table!\n", 'info')
        
        elif self.show_mode == 'fourier' and self.fourier_curve is not None:
            self.equations_text.insert('1.0', "FOURIER SERIES APPROXIMATION\n\n", 'title')
            
            x_fft = self.fourier_curve['x_fft']
            y_fft = self.fourier_curve['y_fft']
            n = self.fourier_curve['n']
            
            harmonics = self.harmonics_var.get()
            
            self.equations_text.insert(tk.END, f"Using {harmonics} harmonics for approximation:\n\n", 'info')
            
            a0_x = np.real(x_fft[0]) / n
            a0_y = np.real(y_fft[0]) / n
            
            x_parts = [f"{a0_x:.6f}"]
            for k in range(1, harmonics + 1):
                an = 2 * np.real(x_fft[k]) / n
                bn = -2 * np.imag(x_fft[k]) / n
                
                if abs(an) > 1e-6:
                    sign = "+ " if an >= 0 else "- "
                    x_parts.append(f"{sign}{abs(an):.6f}·cos({k}·2πt)")
                
                if abs(bn) > 1e-6:
                    if an != 0:
                        sign = "+ " if bn >= 0 else "- "
                    else:
                        sign = "+ " if bn >= 0 else "- "
                    x_parts.append(f"{sign}{abs(bn):.6f}·sin({k}·2πt)")
            
            y_parts = [f"{a0_y:.6f}"]
            for k in range(1, harmonics + 1):
                cn = 2 * np.real(y_fft[k]) / n
                dn = -2 * np.imag(y_fft[k]) / n
                
                if abs(cn) > 1e-6:
                    sign = "+ " if cn >= 0 else "- "
                    y_parts.append(f"{sign}{abs(cn):.6f}·cos({k}·2πt)")
                
                if abs(dn) > 1e-6:
                    if cn != 0:
                        sign = "+ " if dn >= 0 else "- "
                    else:
                        sign = "+ " if dn >= 0 else "- "
                    y_parts.append(f"{sign}{abs(dn):.6f}·sin({k}·2πt)")
            
            self.equations_text.insert(tk.END, "x(t) = ", 'equation')
            x_eq = " ".join(x_parts).replace("+ -", "- ").replace("- -", "+ ")
            self.equations_text.insert(tk.END, x_eq + "\n\n", 'coefficient')
            
            self.equations_text.insert(tk.END, "y(t) = ", 'equation')
            y_eq = " ".join(y_parts).replace("+ -", "- ").replace("- -", "+ ")
            self.equations_text.insert(tk.END, y_eq + "\n\n", 'coefficient')
            
            self.equations_text.insert(tk.END, "\n" + "=" * 80 + "\n\n", 'info')
            self.equations_text.insert(tk.END, "Explanation:\n", 'header')
            
            explanation = """Fourier Series Form:
x(t) = a₀/2 + Σ[aₖ·cos(2πkt) + bₖ·sin(2πkt)]
y(t) = c₀/2 + Σ[cₖ·cos(2πkt) + dₖ·sin(2πkt)]

Where:
• aₖ, bₖ: Cosine and sine coefficients for x(t)
• cₖ, dₖ: Cosine and sine coefficients for y(t)
• k: Harmonic number (frequency = k cycles per unit)
• t: Parameter from 0 to 1 (one complete cycle)"""
            
            self.equations_text.insert(tk.END, explanation + "\n\n", 'info')
            
            self.equations_text.insert(tk.END, "Approximation Quality: ", 'highlight')
            if harmonics < 10:
                self.equations_text.insert(tk.END, "Low (increase harmonics for better fit)\n", 'info')
            elif harmonics < 25:
                self.equations_text.insert(tk.END, "Medium (good balance of accuracy and simplicity)\n", 'info')
            else:
                self.equations_text.insert(tk.END, "High (excellent fit, more complex equation)\n", 'info')
        
        self.equations_text.config(state='disabled')
        self.equations_text.see('1.0')
    
    def change_mode(self):
        self.show_mode = self.mode_var.get()
        
        if self.show_mode == 'fourier' and self.fourier_curve is not None:
            self.controls.pack(fill=tk.X, padx=25, pady=(10, 5), side=tk.BOTTOM)
            self.coeff_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 10), before=self.controls)
            self.status_label.config(text=f"Fourier mode: {self.harmonics_var.get()} harmonics | Scroll to see all coefficients", fg='#e53935')
        else:
            self.controls.pack_forget()
            self.coeff_container.pack_forget()
            if self.is_closed:
                self.status_label.config(text="Parametric mode: Piecewise cubic polynomials", fg='#1e88e5')
            else:
                self.status_label.config(text="Parametric mode: Open curve", fg='#1e88e5')
        
        if self.parametric_curve is not None:
            self.update_equations_display()
            self.render_curve()
    
    def update_harmonics(self, value):
        try:
            n = int(float(value))
            self.harmonics_var.set(n)
            if self.show_mode == 'fourier' and self.fourier_curve is not None:
                self.update_equations_display()
                self.render_curve()
                self.create_coefficients_table()
        except:
            pass
    
    def render_curve(self):
        self.setup_canvas()
        
        if self.parametric_curve is None:
            self.canvas.draw_idle()
            return
        
        t_fine = np.linspace(0, 1, 200)
        
        if self.show_mode == 'parametric':
            x_fine = self.x_spline(t_fine)
            y_fine = self.y_spline(t_fine)
            
            self.ax.plot(x_fine, y_fine, color='#1e88e5', linewidth=3, alpha=0.9, label='Spline')
            
            x = self.parametric_curve['x']
            y = self.parametric_curve['y']
            self.ax.scatter(x, y, color='#ff9800', s=50, alpha=0.7, label='Control Points')
            
            self.ax.legend(loc='upper right', fontsize=9)
            self.ax.set_title("Parametric Cubic Spline", fontsize=14, fontweight='bold', color='#1e88e5')
            
        elif self.show_mode == 'fourier' and self.fourier_curve is not None:
            n = self.fourier_curve['n']
            x_fft = self.fourier_curve['x_fft']
            y_fft = self.fourier_curve['y_fft']
            harmonics = self.harmonics_var.get()
            
            x_fourier = np.real(x_fft[0]) / n
            y_fourier = np.real(y_fft[0]) / n
            
            for k in range(1, harmonics + 1):
                angle = 2 * np.pi * k * t_fine
                x_fourier += (2/n) * (np.real(x_fft[k]) * np.cos(angle) - np.imag(x_fft[k]) * np.sin(angle))
                y_fourier += (2/n) * (np.real(y_fft[k]) * np.cos(angle) - np.imag(y_fft[k]) * np.sin(angle))
            
            self.ax.plot(x_fourier, y_fourier, color='#e53935', linewidth=3, alpha=0.9, 
                        label=f'Fourier ({harmonics} harmonics)')
            
            x_original = self.x_spline(t_fine)
            y_original = self.y_spline(t_fine)
            self.ax.plot(x_original, y_original, color='#1e88e5', linewidth=2, 
                        alpha=0.4, linestyle='--', label='Original')
            
            self.ax.legend(loc='upper right', fontsize=9)
            self.ax.set_title("Fourier Series Approximation", fontsize=14, fontweight='bold', color='#e53935')
        
        self.canvas.draw_idle()
    
    def reset(self):
        self.raw_points = []
        self.drawing = False
        self.parametric_curve = None
        self.fourier_curve = None
        self.is_closed = False
        
        self.setup_canvas()
        self.canvas.draw_idle()
        
        self.show_initial_message()
        self.status_label.config(text="Click and drag to draw your curve", fg='#d4a017')
        self.fourier_radio.config(state='disabled', fg='#cccccc')
        self.mode_var.set('parametric')
        self.show_mode = 'parametric'
        self.controls.pack_forget()
        self.coeff_container.pack_forget()
    
    def copy_equations(self):
        if self.parametric_curve is None:
            messagebox.showinfo("No Equations", "Please draw a curve first!")
            return
        
        self.equations_text.config(state='normal')
        text = self.equations_text.get('1.0', tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text.strip())
        self.equations_text.config(state='disabled')
        
        original_text = self.status_label.cget("text")
        self.status_label.config(text="Equations copied to clipboard!", fg='#43a047')
        self.root.after(2000, lambda: self.status_label.config(text=original_text))

def main():
    root = tk.Tk()
    app = CurveAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
