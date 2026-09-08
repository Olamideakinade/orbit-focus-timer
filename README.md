# Orbit Focus Timer 🪐⏳

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

**Orbit Focus Timer** is a sublime, celestial-themed productivity application built with Python and Tkinter. Transform your workflow by merging the Pomodoro Technique with mesmerizing orbital visualizations and simulated ambient frequency generators.

## ✨ Key Features

- **Celestial Orbital UI:** Watch planets revolve around a central sun timer as your focus session progresses.
- **Customizable Intervals:** Easily switch between Focus Work, Short Break, and Long Break modes.
- **Ambient Focus Tones:** Generate soothing, concentration-enhancing binaural white/pink noise frequencies using pure Python math.
- **Session Analytics:** Track completed deep-work sessions and review daily streak metrics.
- **Audio-Visual Notifications:** Gentle chimes and subtle color shifts alert you when time orbits to a close.

---

## 🚀 Project Structure

```text
orbit-focus-timer/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
└── src/
    ├── __init__.py
    ├── timer.py
    ├── audio.py
    └── ui.py
```

---

## 📦 Prerequisites & Installation

Ensure you have Python 3.8 or higher installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/username/orbit-focus-timer.git
   cd orbit-focus-timer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🕹️ Quickstart & Usage

Run the main application script:

```bash
python main.py
```

### Usage Controls:
- **Start Orbit:** Begins the countdown timer and initiates orbital animation.
- **Pause / Resume:** Halts or continues your current focus cycle.
- **Reset:** Returns the timer to the start of the active mode.
- **Mode Buttons:** Switch instantly between *Focus (25m)*, *Short Break (5m)*, and *Long Break (15m)*.

---

## 🛠️ Architecture & How It Works

- **`main.py`**: Entry point that initializes the application window and orchestrates the module lifecycle.
- **`src/ui.py`**: Custom Tkinter canvas rendering dynamic orbital rings, revolving planets, and sleek controls.
- **`src/timer.py`**: Robust state machine managing time delta decrements, mode switching, and event callbacks.
- **`src/audio.py`**: Lightweight synthesizer generating clean procedural tones and ambient waveforms.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` or the header for more information.
