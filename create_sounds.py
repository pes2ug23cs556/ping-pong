# create_sounds.py
import os
import wave
import struct
import math

# Create folder if it doesn't exist
os.makedirs("assets/sounds", exist_ok=True)

def generate_sine(filename, freq=440, duration=0.15, volume=0.5, samplerate=44100):
    """Generate a simple sine wave .wav file"""
    nframes = int(samplerate * duration)
    amplitude = int(volume * 32767)
    wav = wave.open(filename, 'w')
    wav.setparams((1, 2, samplerate, nframes, 'NONE', 'not compressed'))
    for i in range(nframes):
        t = i / samplerate
        val = int(amplitude * math.sin(2 * math.pi * freq * t))
        data = struct.pack('<h', val)
        wav.writeframesraw(data)
    wav.close()
    print("✅ Created:", filename)

# Paddle hit — bright ping
generate_sine("assets/sounds/paddle_hit.wav", freq=1000, duration=0.1, volume=0.7)

# Wall bounce — low thump
generate_sine("assets/sounds/wall_bounce.wav", freq=600, duration=0.1, volume=0.6)

# Score — short dual tone
def generate_dual(filename, f1=880, f2=660, duration=0.2, volume=0.7, samplerate=44100):
    nframes = int(samplerate * duration)
    amplitude = int(volume * 32767)
    wav = wave.open(filename, 'w')
    wav.setparams((1, 2, samplerate, nframes, 'NONE', 'not compressed'))
    for i in range(nframes):
        t = i / samplerate
        val = int(amplitude * (0.6*math.sin(2*math.pi*f1*t) + 0.4*math.sin(2*math.pi*f2*t)))
        data = struct.pack('<h', val)
        wav.writeframesraw(data)
    wav.close()
    print("✅ Created:", filename)

generate_dual("assets/sounds/score.wav")

# Winning sound — higher pitch, longer duration
generate_sine("assets/sounds/win.wav", freq=1200, duration=0.5, volume=0.8)
