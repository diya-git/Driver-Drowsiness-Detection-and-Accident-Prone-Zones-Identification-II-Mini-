import numpy as np
import wave
import struct

# Parameters
frequency = 1000  # Hz
duration = 1      # seconds
sample_rate = 44100
amplitude = 32767

num_samples = int(sample_rate * duration)

with wave.open("alarm.wav", "w") as wav_file:
    wav_file.setparams((1, 2, sample_rate, num_samples, "NONE", "not compressed"))

    for i in range(num_samples):
        value = int(amplitude * np.sin(2 * np.pi * frequency * i / sample_rate))
        data = struct.pack("<h", value)
        wav_file.writeframesraw(data)

print("alarm.wav generated successfully!")
