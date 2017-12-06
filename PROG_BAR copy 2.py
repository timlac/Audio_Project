from __future__ import print_function
import sys
import re
import time


class Meter(object):
    # DEFAULT = 'Progress: %(bar)s %(percent)3d%%'
    # # FULL = '%(bar)s %(current)d/%(total)d (%(percent)3d%%) %(remaining)d to go'
    # dBFS = 'RMS/dBFS: %(bar)s %(db)3d%%' # replace %(percent)3d%% with the dBFS value
    dBFS = 'dBFS: %(db)3d%% \n %(bar)s ' # replace %(percent)3d%% with the dBFS value

    def __init__(self, total, rms=0, db=0, width=50, fmt=dBFS, symbol='*',
                 output=sys.stderr):
        assert len(symbol) == 1

        self.total = total
        self.width = width
        self.symbol = symbol
        self.output = output
        # self.fmt = re.sub(r'(?P<name>%\(.+?\))d',
        #     r'\g<name>%dd' % len(str(total)), fmt)
        self.fmt = fmt

        self.current = 0

    def __call__(self, rms = 0, db = 0):
        self.current = rms
        # db = db
        # percent = self.current / float(self.total)
        size = int(self.width * self.current * 2)
        # remaining = self.total - self.current
        bar = '[' + self.symbol * size + ' ' * (self.width - size) + ']'

        args = {
            'rms': rms,
            'db': db,
            'total': self.total,
            'bar': bar,
            'current': self.current,
            # 'percent': percent * 100,
            # 'remaining': remaining
        }
        print('\r' + self.fmt % args, file=self.output, end='')

    def done(self):
        self.current = self.total
        self()
        print('', file=self.output)


###############

# progress = Meter(10, fmt=Meter.FULL)
if __name__ == "__main__":
    meter = Meter(10, fmt=Meter.dBFS)

    for x in xrange(meter.total):
        meter.current += 1
        meter()
        time.sleep(0.1)
    meter.done()