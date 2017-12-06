"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys

print("playing my file")

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)

# readframes() -- returns at most n frames of audio
# en frame är en snapshot i tiden, left and right
# pa.paContinue #: There is more audio data to come

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

# open stream using callback (3)

# format -- has something to do with sample width
# channels -- returns number of audio channels (1 for mono, 2 for stereo)
# rate -- returns sampling frequency
# A stream can either be input, output, or both.

# :param
# To use non - blocking operation, specify a callback that conforms to the following signtature
#
# callback(in_data,  # recorded data if input=True; else None
#          frame_count,  # number of frames
#          time_info,  # dictionary
#          status_flags)  # PaCallbackFlags

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

def pause_play():
    input("press enter to stop stream")
    stream.stop_stream()
    input("press enter to start stream again")
    stream.start_stream()
    return

def choose_time():
    sample_rate = 44100

    try:
        start_sek = int(input("input the part of the song you want to start playing at"))
        end_sek = int(input("input the time you want to the song to stop playing at"))
    except ValueError:
            print("that is not a number!")

    start = start_sek * sample_rate
    end = end_sek * sample_rate

    return start, end

stream.stop_stream()

start, end = choose_time()

wf.setpos(start)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    pause_play()


# stop stream (6)
stream.stop_stream()

stream.close()
wf.close()

# close PyAudio (7)
p.terminate()
