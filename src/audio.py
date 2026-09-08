"""
Procedural audio tone generator for notifications and ambient focus.
"""
import math
import struct

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

class SoundSynthesizer:
    @staticmethod
    def generate_beep(frequency=440, duration_ms=300, volume=0.5):
        """Returns raw PCM byte string for a simple sine wave tone if numpy is available."""
        if not HAS_NUMPY:
            return b""
        sample_rate = 22050
        num_samples = int(sample_rate * (duration_ms / 1000.0))
        t = np.linspace(0, duration_ms / 1000.0, num_samples, endpoint=False)
        wave = volume * np.sin(2 * np.pi * frequency * t)
        # Apply simple fade in/out to avoid clicking
        fade = int(sample_rate * 0.01)
        if num_samples > fade * 2:
            wave[:fade] *= np.linspace(0, 1, fade)
            wave[-fade:] *= np.linspace(1, 0, fade)
        
        audio_data = (wave * 32767).astype(np.int16)
        return audio_data.tobytes()

    @staticmethod
    def generate_ambient_noise(duration_seconds=5, volume=0.2):
        """Generates pink/white ambient noise buffer for focus support."""
        if not HAS_NUMPY:
            return b""
        sample_rate = 22050
        num_samples = sample_rate * duration_seconds
        noise = np.random.normal(0, 1, num_samples)
        # Simple low-pass filter simulation via cumulative sum for pink-ish tint
        pink_noise = np.cumsum(noise)
        pink_noise -= np.mean(pink_noise)
        max_val = np.max(np.abs(pink_noise))
        if max_val > 0:
            pink_noise = pink_noise / max_val
        audio_data = (pink_noise * volume * 32767).astype(np.int16)
        return audio_data.tobytes()
