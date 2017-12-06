from __future__ import print_function
import sys
import re
import time

def asdf():
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    for i in xrange(toolbar_width):
        time.sleep(0.1) # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("\n")


class Meter(object):
    # DEFAULT = 'Progress: %(bar)s %(percent)3d%%'
    # # FULL = '%(bar)s %(current)d/%(total)d (%(percent)3d%%) %(remaining)d to go'
    # dBFS = 'RMS/dBFS: %(bar)s %(db)3d%%' # replace %(percent)3d%% with the dBFS value
    dBFS = 'dBFS: %(db)3d %% %(bar)s ' # replace %(percent)3d%% with the dBFS value

    def __init__(self, total, rms=0, db=0, width=100, fmt=dBFS, symbol='*', output=sys.stderr):
        assert len(symbol) == 1
        # self.total = total
        self.width = width
        self.symbol = symbol
        self.output = output
        self.fmt = fmt
        self.rms = rms
        self.db = 0

    def __call__(self, rms = 0, db = 0):
        self.rms = rms
        # db = db
        # percent = self.rms / float(self.total)
        size = int(self.width * self.rms)
        bar = '[' + self.symbol * size + ' ' * (self.width - size) + ']'

        args = {
            'rms': rms,
            'db': db,
            # 'total': self.total,
            'bar': bar,
            'rms': self.rms,
        }
        #print('\r' + self.fmt % args, file=self.output, end='')
        # print(self.fmt % args)
        # print('dBFS: %(db)3d %(bar)s ' % args)
        sys.stdout.write('\rdBFS: %(db)3d %(bar)s ' % args)
        sys.stdout.flush()


    # def done(self):
    #     # self.rms = self.total
    #     self() # ???
    #     print('', file=self.output)

if __name__ == "__main__":
    meter = Meter(10, fmt=Meter.dBFS)

    # for x in xrange(meter.total):
    #     meter.rms += 1
    #     meter()
    #     time.sleep(0.1)
    # meter.done()