"""PyAudio Example: Play a wave file."""

import pyaudio # https://people.csail.mit.edu/hubert/pyaudio/docs/#id1
import wave # https://docs.python.org/2/library/wave.html
import sys # https://docs.python.org/3/library/sys.html

CHUNK = 1024

# sys.argv = The list of command line arguments passed to a Python script. argv[0] is the script name (it is operating system dependent whether this is a full pathname or not). If the command was executed using the -c command line option to the interpreter, argv[0] is set to the string '-c'. If no script name was passed to the Python interpreter, argv[0] is the empty string. To loop over the standard input, or the list of files given on the command line, see the fileinput module.
if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1) # https://stackoverflow.com/questions/44893807/i-want-to-know-what-exactly-sys-exit-1-returns-in-python?noredirect=1&lq=1

# read only
wf = wave.open(sys.argv[1], 'rb')
# wf.setpos(60*44100) wave.getframerate())

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), 
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
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
