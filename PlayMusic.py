#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import sys
from PyQt5.QtWidgets import (QWidget, QProgressBar,
                             QApplication, QPushButton, QSlider)
from PyQt5.QtCore import Qt
import threading
import queue
import time
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import ComputeRmsDB
from ComputeRmsDB import Meter

class Buffering:
    # total number of buffers
    total = 4
    buffer = queue.Queue()

    @classmethod
    def set_total(cls, total):
        cls.total = total

    @classmethod
    def flush_buffers(cls):
        # freeze threads and clear buffer
        # (mutex = freeze threads)
        cls.buffer.queue.clear()

    @classmethod
    def load_buffers(cls, framecount):
        for i in range(cls.total-1):
            cls.buffer.put( wf.readframes(framecount))

    @classmethod
    def callback(cls, in_data, frame_count, time_info, status):
        # only start new threads if buffer queue size is smaller than 5
        # in practice this will never happen with only Double buffering (total = 2)
        if cls.buffer.qsize() < 10:
            # start thread to load buffers
            threading.Thread(target=cls.load_buffers, args=(frame_count,)).start()
        # get next data frame

        data = cls.buffer.get()

        # INSERT
        rms_db = ComputeRmsDB.get_rms(data)  # GET RMS & DB
        decibel_meter(rms=rms_db['rms'],
                      db=rms_db['db'])  # UPDATE METER
        # INSERT

        return ( data, pyaudio.paContinue )

#Inherit from QThread
class Worker(QtCore.QThread):

    #This is the signal that will be emitted during the processing.
    #By including int as an argument, it lets the signal know to expect
    #an integer argument when emitting.
    update_progress = pyqtSignal(int)

    #You can do any extra things in this init you need, but for this example
    #nothing else needs to be done expect call the super's init
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.pause = False

    #A QThread is run by calling it's start() function, which calls this run()
    #function in it's own "thread".
    def run(self):
        while(get_current_time() <= duration):
            if not self.pause:
                self.update_progress.emit(get_current_time())
            time.sleep(0.1)

class MusicPlayer(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # pause play button
        self.pause_play_button = QPushButton('Pause Play', self)
        self.pause_play_button.setCheckable(True)
        self.pause_play_button.move(10, 10)
        self.pause_play_button.clicked[bool].connect(self.handle_clicks)

        # progress bar
        self.pbar = QProgressBar(self)
        self.pbar.setFormat("%v")
        self.pbar.setMaximum(get_duration())
        self.pbar.setGeometry(50, 80, 400, 25)

        # slider
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setMaximum(get_duration())
        self.sld.setGeometry(50, 40, 400, 25)

        self.worker = Worker()
        self.worker.update_progress.connect(self.set_progress)
        self.worker.start()

        # self.c.update_pbar[int].connect(self.pbar.setValue)
        self.sld.sliderReleased.connect(self.change_value)

        # configure placements in window
        self.setGeometry(300, 300, 500, 170)
        self.setWindowTitle('Music Player')
        self.show()

    def set_progress(self, progress):
        self.pbar.setValue(progress)

    def change_value(self):
        self.worker.pause = True
        stream.stop_stream()
        set_song_pos(self.sld.value())
        stream.start_stream()
        self.worker.pause = False

    def handle_clicks(self, pressed):
        source = self.sender()
        if source.text() == "Pause Play":
            toggle_stream()

def initialize_stream():
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=Buffering.callback)

    stream.stop_stream()
    return stream

def toggle_stream():
    if stream.is_active():
        stream.stop_stream()
    else:
        stream.start_stream()

def get_current_time():
    curr_time = wf.tell() / wf.getframerate()
    return curr_time

def get_duration():
    return wf.getnframes() / float(wf.getframerate())

def set_song_pos(set_time):
    wf.setpos(set_time * wf.getframerate())

def filehandle():
    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        sys.exit(-1)

    wf = wave.open(sys.argv[1], 'rb')

    return wf

# INSTANTIATE METER
decibel_meter = Meter()

Buffering.set_total(5)

lock = threading.Lock()

wf = filehandle()

duration = get_duration()

stream = initialize_stream()

app = QApplication(sys.argv)
ex = MusicPlayer()

sys.exit(app.exec_())
