"""
Graphical User Interface using Tkinter with celestial canvas animations.
"""
import tkinter as tk
from tkinter import font as tkfont
import math

from src.timer import FocusTimer, MODE_FOCUS, MODE_SHORT_BREAK, MODE_LONG_BREAK

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
        
        self.setup_styles()
        self.create_widgets()
        
        # Animation angle for planet orbit
        self.orbit_angle = 0.0
        
        # Start loop
        self.update_loop()

    def setup_styles(self):
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.time_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self.body_font = tkfont.Font(family="Helvetica", size=12)

    def create_widgets(self):
        # Top Mode Selection Frame
        mode_frame = tk.Frame(self.root, bg=BG_COLOR)
        mode_frame.pack(pady=15)
        
        self.mode_buttons = {}
        for mode in [MODE_FOCUS, MODE_SHORT_BREAK, MODE_LONG_BREAK]:
            btn = tk.Button(
                mode_frame, text=mode, font=self.body_font, bg=BTN_BG, fg=TEXT_COLOR,
                activebackground=ACCENT_COLOR, activeforeground=TEXT_COLOR, relief="flat",
                padx=10, pady=5, command=lambda m=mode: self.change_mode(m)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.mode_buttons[mode] = btn
            
        self.highlight_active_mode_btn(MODE_FOCUS)

        # Canvas for Celestial Orbit Animation
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Timer Display Label inside canvas or below
        self.time_label = tk.Label(
            self.root, text="25:00", font=self.time_font, bg=BG_COLOR, fg=TEXT_COLOR
        )
        self.time_label.pack(pady=5)
        
        # Stats Label
        self.stats_label = tk.Label(
            self.root, text="Sessions Completed: 0", font=self.body_font, bg=BG_COLOR, fg=TEXT_COLOR
        )
        self.stats_label.pack(pady=5)

        # Controls Frame
        control_frame = tk.Frame(self.root, bg=BG_COLOR)
        control_frame.pack(pady=15)
        
        self.start_btn = tk.Button(
            control_frame, text="Start Orbit", font=self.body_font, bg=ACCENT_COLOR, fg=TEXT_COLOR,
            relief="flat", padx=20, pady=8, command=self.toggle_start
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(
            control_frame, text="Reset", font=self.body_font, bg=BTN_BG, fg=TEXT_COLOR,
            relief="flat", padx=20, pady=8, command=self.reset_timer
        )
        reset_btn.pack(side=tk.LEFT, padx=10)

    def highlight_active_mode_btn(self, active_mode):
        for mode, btn in self.mode_buttons.items():
            if mode == active_mode:
                btn.configure(bg=ACCENT_COLOR)
            else:
                btn.configure(bg=BTN_BG)

    def change_mode(self, mode):
        self.timer.set_mode(mode)
        self.highlight_active_mode_btn(mode)
        self.update_display()

    def toggle_start(self):
        if self.timer.running:
            self.timer.pause()
            self.start_btn.configure(text="Resume Orbit", bg=ACCENT_COLOR)
        else:
            self.timer.start()
            self.start_btn.configure(text="Pause Orbit", bg="#EF4444")

    def reset_timer(self):
        self.timer.reset()
        self.start_btn.configure(text="Start Orbit", bg=ACCENT_COLOR)
        self.update_display()

    def on_tick(self, time_left):
        self.update_display()

    def on_complete(self, mode):
        self.start_btn.configure(text="Start Orbit", bg=ACCENT_COLOR)
        self.stats_label.configure(text=f"Sessions Completed: {self.timer.sessions_completed}")

    def update_display(self):
        mins = self.timer.time_left // 60
        secs = self.timer.time_left % 60
        self.time_label.configure(text=f"{mins:02d}:{secs:02d}")

    def draw_celestial(self):
        self.canvas.delete("all")
        cx, cy = 150, 150
        sun_radius = 35
        orbit_radius = 90
        
        # Draw orbit path
        self.canvas.create_oval(
            cx - orbit_radius, cy - orbit_radius,
            cx + orbit_radius, cy + orbit_radius,
            outline=ORBIT_COLOR, width=2
        )
        
        # Draw Sun
        self.canvas.create_oval(
            cx - sun_radius, cy - sun_radius,
            cx + sun_radius, cy + sun_radius,
            fill=SUN_COLOR, outline=""
        )
        
        # Draw Planet
        if self.timer.duration > 0:
            progress = 1.0 - (self.timer.time_left / self.timer.duration)
            self.orbit_angle = progress * 2 * math.pi
            
        px = cx + orbit_radius * math.cos(self.orbit_angle)
        py = cy + orbit_radius * math.sin(self.orbit_angle)
        planet_radius = 12
        
        self.canvas.create_oval(
            px - planet_radius, py - planet_radius,
            px + planet_radius, py + planet_radius,
            fill=PLANET_COLOR, outline=""
        )

    def update_loop(self):
        self.timer.tick()
        self.draw_celestial()
        self.root.after(1000, self.update_loop)

    def run(self):
        self.root.mainloop()
