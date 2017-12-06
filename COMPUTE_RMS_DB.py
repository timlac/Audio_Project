############### TOOLBAR
# python program_one_callback.py 121_prog_sooftish\ 1.wav

from __future__ import print_function
import sys
import re
import pyaudio
import time
import math
import struct
import sys

# import PROG_BAR


FORMAT = pyaudio.paInt16 # why is this neeeded ?
SHORT_NORMALIZE = (1.0/32768.0) # ?


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
    rms = math.sqrt( sum_squares / count )
    # dB = 20 * log10(amplitude)
    db = 20 * math.log10(rms)
    # print( db )
    return {'rms':rms, 'db':db } #math.sqrt( sum_squares / count )





