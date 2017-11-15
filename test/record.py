"""
PyAudio example: Record a few seconds of audio and save to a WAVE
file.
"""

import pyaudio
import wave
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

if sys.platform == 'darwin': # os x
    CHANNELS = 1

p = pyaudio.PyAudio() # instantiate pyaudio

# To record or play audio, open a stream on the desired device with the desired audio parameters using pyaudio.PyAudio.open() (2). This sets up a pyaudio.Stream to play or record audio.
stream = p.open(format=FORMAT, 
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames)) # https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
wf.close()
