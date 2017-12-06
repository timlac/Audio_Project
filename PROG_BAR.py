import sys
import time

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