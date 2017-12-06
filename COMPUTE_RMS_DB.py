############### TOOLBAR
# python program_one_callback.py 121_prog_sooftish\ 1.wav

from __future__ import print_function
import sys
import pyaudio
import time
import math
import struct
import sys
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0) # ?


def get_rms( block ):
    # RMS amplitude is defined as the square root of the mean over time of the square of the amplitude. so we need to convert this string of bytes into a string of 16-bit samples...
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

class Meter(object):
    def __init__(self, total, rms=0, db=0, width=100, symbol='*'):
        assert len(symbol) == 1
        self.width = width
        self.symbol = symbol
        self.rms = rms
        self.db = 0

    def __call__(self, rms = 0, db = 0):
        self.rms = rms
        self.db = db
        size = int(self.width * self.rms)
        bar = '[' + self.symbol * size + ' ' * (self.width - size) + ']'

        args = { 'rms': rms,    'db': db,   'bar': bar, 'rms': self.rms, }
        
        sys.stdout.write('\rdBFS: %(db)3d %(bar)s ' % args)
        sys.stdout.flush()



