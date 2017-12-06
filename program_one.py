"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)

# format -- has something to do with sample width
# channels -- returns number of audio channels (1 for mono, 2 for stereo)
# rate -- returns sampling frequency
# A stream can either be input, output, or both.
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

def choose_time():
    global wf

    try:
        desired_time = int( input("input the part of the song you want to start playing at") )
    except not desired_time or not desired_time.isnumeric():
        print("that is not a number!")

    location = (desired_time * 44100)

    wf.setpos(location)

# read data
# readframes() -- returns at most n frames of audio
# en frame är en snapshot i tiden, left and right

choose_time()

data = wf.readframes(CHUNK)

# play stream (3)
while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()