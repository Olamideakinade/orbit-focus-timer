"""
Procedural audio tone generator for notifications and ambient focus.
"""
import math

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

class SoundSynthesizer:
    @staticmethod
    def generate_beep(frequency=440, duration_ms=300, volume=0.5):
        """Returns raw PCM sample array (or tuple) for a simple sine wave tone if numpy is available."""
        if not HAS_NUMPY:
            return None
        sample_rate = 22050
        num_samples = int(sample_rate * (duration_ms / 1000.0))
        t = np.linspace(0, duration_ms / 1000.0, num_samples, endpoint=False)
        wave = volume * np.sin(2 * np.pi * frequency * t)
        # Apply simple fade out to prevent clicking
        fade = np.linspace(1, 0, int(sample_rate * 0.05))
        if len(fade) < len(wave):
            wave[-len(fade):] *= fade
        return (wave * 32767).astype(np.int16)
