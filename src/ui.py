"""
Graphical User Interface using Tkinter with celestial canvas animations.
"""
import tkinter as tk
from tkinter import font as tkfont
import math

from src.timer import FocusTimer, MODE_FOCUS, MODE_SHORT_BREAK, MODE_LONG_BREAK
from src.audio import SoundSynthesizer

BG_COLOR = "#0B0F19"
SUN_COLOR = "#F59E0B"
ORBIT_COLOR = "#1E293B"
PLANET_COLOR = "#38BDF8"
TEXT_COLOR = "#F8FAFC"
ACCENT_COLOR = "#6366F1"
BTN_BG = "#1E293B"

class OrbitApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Orbit Focus Timer")
        self.root.geometry("500x650")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.timer = FocusTimer(on_tick=self.on_tick, on_complete=self.on_complete)
        self.angle = 0.0

        self.setup_styles()
        self.setup_ui()
        self.update_clock_display(self.timer.time_left)
        self.animate_orbit()
        self.schedule_timer_loop()

    def setup_styles(self):
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.time_font = tkfont.Font(family="Helvetica", size=36, weight="bold")
        self.btn_font = tkfont.Font(family="Helvetica", size=11, weight="bold")

    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=BG_COLOR)
        header_frame.pack(pady=15)

        self.title_label = tk.Label(header_frame, text="Orbit Focus Timer", font=self.title_font, fg=TEXT_COLOR, bg=BG_COLOR)
        self.title_label.pack()

        # Mode Selection Buttons
        mode_frame = tk.Frame(self.root, bg=BG_COLOR)
        mode_frame.pack(pady=10)

        self.mode_buttons = {}
        for mode in [MODE_FOCUS, MODE_SHORT_BREAK, MODE_LONG_BREAK]:
            btn = tk.Button(mode_frame, text=mode, font=self.btn_font, fg=TEXT_COLOR, bg=BTN_BG,
                            activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR,
                            bd=0, padx=10, pady=5, command=lambda m=mode: self.change_mode(m))
            btn.pack(side=tk.LEFT, padx=5)
            self.mode_buttons[mode] = btn

        self.highlight_active_mode()

        # Canvas for Orbital Animation
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(pady=10)

        # Timer Display Label inside canvas or overlay
        self.time_label = tk.Label(self.root, text="25:00", font=self.time_font, fg=TEXT_COLOR, bg=BG_COLOR)
        self.time_label.pack(pady=5)

        # Control Buttons
        ctrl_frame = tk.Frame(self.root, bg=BG_COLOR)
        ctrl_frame.pack(pady=15)

        self.start_btn = tk.Button(ctrl_frame, text="Start Orbit", font=self.btn_font, fg=TEXT_COLOR, bg=ACCENT_COLOR,
                                   activebackground=SUN_COLOR, activeforeground=TEXT_COLOR, bd=0, padx=20, pady=8,
                                   command=self.toggle_start)
        self.start_btn.pack(side=tk.LEFT, padx=10)

        reset_btn = tk.Button(ctrl_frame, text="Reset", font=self.btn_font, fg=TEXT_COLOR, bg=BTN_BG,
                              activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR, bd=0, padx=20, pady=8,
                              command=self.reset_timer)
        reset_btn.pack(side=tk.LEFT, padx=10)

        # Stats Label
        self.stats_label = tk.Label(self.root, text="Orbits Completed: 0", font=("Helvetica", 10), fg="#94A3B8", bg=BG_COLOR)
        self.stats_label.pack(pady=10)

    def change_mode(self, mode):
        self.timer.set_mode(mode)
        self.highlight_active_mode()
        self.update_clock_display(self.timer.time_left)
        self.start_btn.config(text="Start Orbit")

    def highlight_active_mode(self):
        for mode, btn in self.mode_buttons.items():
            if mode == self.timer.mode:
                btn.config(bg=ACCENT_COLOR)
            else:
                btn.config(bg=BTN_BG)

    def toggle_start(self):
        if self.timer.running:
            self.timer.pause()
            self.start_btn.config(text="Start Orbit")
        else:
            self.timer.start()
            self.start_btn.config(text="Pause")

    def reset_timer(self):
        self.timer.reset()
        self.start_btn.config(text="Start Orbit")
        self.update_clock_display(self.timer.time_left)

    def on_tick(self, time_left):
        self.update_clock_display(time_left)

    def on_complete(self, mode):
        self.start_btn.config(text="Start Orbit")
        SoundSynthesizer.generate_beep(frequency=587.33, duration_ms=500)
        if mode == MODE_FOCUS:
            self.stats_label.config(text=f"Orbits Completed: {self.timer.sessions_completed}")

    def update_clock_display(self, seconds):
        mins, secs = divmod(seconds, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        self.time_label.config(text=time_str)

    def animate_orbit(self):
        self.canvas.delete("all")
        cx, cy = 150, 150
        sun_radius = 35
        orbit_radius = 90

        # Draw Sun
        self.canvas.create_oval(cx - sun_radius, cy - sun_radius, cx + sun_radius, cy + sun_radius,
                                fill=SUN_COLOR, outline="")

        # Draw Orbit Ring
        self.canvas.create_oval(cx - orbit_radius, cy - orbit_radius, cx + orbit_radius, cy + orbit_radius,
                                outline=ORBIT_COLOR, width=2)

        # Draw Planet if running
        if self.timer.running:
            self.angle += 0.03

        px = cx + orbit_radius * math.cos(self.angle)
        py = cy + orbit_radius * math.sin(self.angle)
        planet_radius = 10
        self.canvas.create_oval(px - planet_radius, py - planet_radius, px + planet_radius, py + planet_radius,
                                fill=PLANET_COLOR, outline="")

        self.root.after(30, self.animate_orbit)

    def schedule_timer_loop(self):
        self.timer.tick()
        self.root.after(1000, self.schedule_timer_loop)

    def run(self):
        self.root.mainloop()
