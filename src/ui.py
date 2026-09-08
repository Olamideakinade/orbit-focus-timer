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
        self.root.geometry("500	600")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.timer = FocusTimer(on_tick=self.update_timer_display, on_complete=self.handle_completion)
        
        self.angle = 0.0

        self.setup_fonts()
        self.setup_widgets()
        self.schedule_loop()

    def setup_fonts(self):
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.time_font = tkfont.Font(family="Helvetica", size=36, weight="bold")
        self.stat_font = tkfont.Font(family="Helvetica", size=11)
        self.btn_font = tkfont.Font(family="Helvetica", size=11, weight="bold")

    def setup_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=BG_COLOR)
        header_frame.pack(pady=20)
        
        self.title_label = tk.Label(
            header_frame, text="ORBIT FOCUS TIMER", font=self.title_font, fg=TEXT_COLOR, bg=BG_COLOR
        )
        self.title_label.pack()

        # Canvas for Celestial Animation
        self.canvas = tk.Canvas(
            self.root, width=300, height=300, bg=BG_COLOR, highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # Timer Display Label inside canvas center
        self.time_label = tk.Label(
            self.root, text="25:00", font=self.time_font, fg=TEXT_COLOR, bg=BG_COLOR
        )
        self.time_label.place(relx=0.5, rely=0.42, anchor="center")

        # Mode Switch Buttons
        mode_frame = tk.Frame(self.root, bg=BG_COLOR)
        mode_frame.pack(pady=10)

        self.btn_focus = tk.Button(
            mode_frame, text="Focus", command=lambda: self.change_mode(MODE_FOCUS),
            font=self.btn_font, fg=TEXT_COLOR, bg=ACCENT_COLOR, bd=0, padx=10, pady=5
        )
        self.btn_focus.grid(row=0, column=0, padx=5)

        self.btn_short = tk.Button(
            mode_frame, text="Short Break", command=lambda: self.change_mode(MODE_SHORT_BREAK),
            font=self.btn_font, fg=TEXT_COLOR, bg=BTN_BG, bd=0, padx=10, pady=5
        )
        self.btn_short.grid(row=0, column=1, padx=5)

        self.btn_long = tk.Button(
            mode_frame, text="Long Break", command=lambda: self.change_mode(MODE_LONG_BREAK),
            font=self.btn_font, fg=TEXT_COLOR, bg=BTN_BG, bd=0, padx=10, pady=5
        )
        self.btn_long.grid(row=0, column=2, padx=5)

        # Control Buttons
        ctrl_frame = tk.Frame(self.root, bg=BG_COLOR)
        ctrl_frame.pack(pady=15)

        self.btn_start = tk.Button(
            ctrl_frame, text="Start Orbit", command=self.toggle_start,
            font=self.btn_font, fg=TEXT_COLOR, bg="#10B981", bd=0, width=12, pady=8
        )
        self.btn_start.grid(row=0, column=0, padx=8)

        self.btn_reset = tk.Button(
            ctrl_frame, text="Reset", command=self.reset_timer,
            font=self.btn_font, fg=TEXT_COLOR, bg="#EF4444", bd=0, width=10, pady=8
        )
        self.btn_reset.grid(row=0, column=1, padx=8)

        # Stats Label
        self.stats_label = tk.Label(
            self.root, text="Sessions Completed: 0", font=self.stat_font, fg="#94A3B8", bg=BG_COLOR
        )
        self.stats_label.pack(pady=10)

    def draw_orbit(self):
        self.canvas.delete("all")
        cx, cy = 150, 150
        sun_radius = 35
        orbit_radius = 110

        # Draw Sun
        self.canvas.create_oval(
            cx - sun_radius, cy - sun_radius, cx + sun_radius, cy + sun_radius,
            fill=SUN_COLOR, outline=""
        )

        # Draw Orbit Ring
        self.canvas.create_oval(
            cx - orbit_radius, cy - orbit_radius, cx + orbit_radius, cy + orbit_radius,
            outline=ORBIT_COLOR, width=2
        )

        # Calculate Planet Position
        if self.timer.running:
            self.angle += 0.03

        px = cx + orbit_radius * math.cos(self.angle)
        py = cy + orbit_radius * math.sin(self.angle)
        planet_radius = 10

        # Draw Planet
        self.canvas.create_oval(
            px - planet_radius, py - planet_radius, px + planet_radius, py + planet_radius,
            fill=PLANET_COLOR, outline=""
        )

    def update_timer_display(self, time_left, duration):
        mins = time_left // 60
        secs = time_left % 60
        self.time_label.config(text=f"{mins:02d}:{secs:02d}")

    def toggle_start(self):
        if self.timer.running:
            self.timer.pause()
            self.btn_start.config(text="Resume Orbit", bg="#10B981")
        else:
            self.timer.start()
            self.btn_start.config(text="Pause Orbit", bg="#F59E0B")

    def reset_timer(self):
        self.timer.reset()
        self.update_timer_display(self.timer.time_left, self.timer.duration)
        self.timer.running = False
        self.btn_start.config(text="Start Orbit", bg="#10B981")

    def change_mode(self, mode):
        self.timer.set_mode(mode)
        self.update_timer_display(self.timer.time_left, self.timer.duration)
        self.btn_start.config(text="Start Orbit", bg="#10B981")

        # Highlight active mode button
        for btn, m in [(self.btn_focus, MODE_FOCUS), (self.btn_short, MODE_SHORT_BREAK), (self.btn_long, MODE_LONG_BREAK)]:
            if m == mode:
                btn.config(bg=ACCENT_COLOR)
            else:
                btn.config(bg=BTN_BG)

    def handle_completion(self, mode):
        self.btn_start.config(text="Start Orbit", bg="#10B981")
        self.stats_label.config(text=f"Sessions Completed: {self.timer.sessions_completed}")

    def schedule_loop(self):
        self.timer.tick()
        self.draw_orbit()
        self.root.after(100, self.schedule_loop)

    def run(self):
        self.root.mainloop()
