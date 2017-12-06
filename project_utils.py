############### TOOLBAR
# python program_one_callback.py 121_prog_sooftish\ 1.wav

import pyaudio
import time
import math
import struct
import sys

FORMAT = pyaudio.paInt16 # why is this neeeded ?
SHORT_NORMALIZE = (1.0/32768.0) # ?

# toolbar_width = 40
def print_frame(data):
    type(data)

# setup toolbar
def display_amplitude(frames):
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    for i in xrange(toolbar_width):
        time.sleep(0.1) # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("\n")


def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n
    amp = math.sqrt( sum_squares / count )
    print( amp )
    return #math.sqrt( sum_squares / count )





