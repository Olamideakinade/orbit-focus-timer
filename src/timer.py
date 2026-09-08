"""
Timer state machine and logic module.
"""
import time

MODE_FOCUS = "Focus"
MODE_SHORT_BREAK = "Short Break"
MODE_LONG_BREAK = "Long Break"

TIMES = {
    MODE_FOCUS: 25 * 60,
    MODE_SHORT_BREAK: 5 * 60,
    MODE_LONG_BREAK: 15 * 60
}

class FocusTimer:
    def __init__(self, on_tick=None, on_complete=None):
        self.mode = MODE_FOCUS
        self.duration = TIMES[self.mode]
        self.time_left = self.duration
        self.running = False
        
        self.on_tick = on_tick
        self.on_complete = on_complete
        
        self.sessions_completed = 0

    def set_mode(self, mode):
        if mode in TIMES:
            self.mode = mode
            self.duration = TIMES[mode]
            self.time_left = self.duration
            self.running = False

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.time_left = self.duration

    def tick(self):
        if self.running:
            if self.time_left > 0:
                self.time_left -= 1
                if self.on_tick:
                    self.on_tick(self.time_left, self.duration)
                
                if self.time_left == 0:
                    self.running = False
                    if self.mode == MODE_FOCUS:
                        self.sessions_completed += 1
                    if self.on_complete:
                        self.on_complete(self.mode)
