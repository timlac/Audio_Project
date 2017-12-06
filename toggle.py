#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import sys
import time
import threading
from PyQt5.QtCore import Qt,QObject
from PyQt5.QtWidgets import (QWidget, QProgressBar,
                             QApplication, QPushButton, QSlider)


def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

def choose_time():
    try:
        start_sek = int(input("input the part of the song you want to start playing at"))
        end_sek = int(input("input the time you want to the song to stop playing at"))
    except ValueError:
            print("that is not a number!")

    start = start_sek * sample_rate
    end = end_sek * sample_rate

    return start, end

def filehandle():
    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        sys.exit(-1)

    wf = wave.open(sys.argv[1], 'rb')

    return wf

def initialize_stream():
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.stop_stream()
    return stream

def get_duration():
    frames = wf.getnframes()
    rate = wf.getframerate()
    duration = frames / float(rate)
    return duration

def get_current_time():
    curr_time = wf.tell() / wf.getframerate()
    return curr_time

def toggle_stream():
    if stream.is_active():
        stream.stop_stream()
    else:
        stream.start_stream()

def set_song_pos(set_time):
    wf.setpos(set_time*sample_rate)



"""
ZetCode PyQt5 tutorial

In this example, we create three toggle buttons.
They will control the background color of a
QFrame.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

from PyQt5.QtCore import Qt, pyqtSignal

class Communicate(QObject):
    update_pbar = pyqtSignal(int)

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        # self.pbar_thread = threading.Thread(target=self.update_bars)
        # self.pbar_thread.start()

    def initUI(self):

        # pause play button
        pause_play_button = QPushButton('Pause Play', self)
        pause_play_button.setCheckable(True)
        pause_play_button.move(10, 10)
        pause_play_button.clicked[bool].connect(self.handleClicks)

        # progress bar
        self.pbar = QProgressBar(self)
        self.pbar.setFormat("%v")
        self.pbar.setMaximum(get_duration())
        self.pbar.setGeometry(50, 80, 200, 25)

        # slider
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setMaximum(get_duration())
        self.sld.setGeometry(50, 40, 200, 25)

        # connect slider and progress bar
        self.c = Communicate()
        self.c.update_pbar[int].connect(self.pbar.setValue)
        self.sld.valueChanged[int].connect(self.changeValue)

        # configure placements in window
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Music Player')
        self.show()

    # def update_bars(self, current_time=None):
    #     cv.wait()
    #     while get_current_time() < duration:
    #         self.sld.setValue(get_current_time())
    #     cv.notify_all()

    def changeValue(self, value):

        self.c.update_pbar.emit(value)
        self.pbar.repaint()
        set_song_pos(value)



    def handleClicks(self, pressed):
        source = self.sender()
        if source.text() == "Pause Play":
            toggle_stream()


# lock = threading.Lock()
# cv = threading.Condition(lock)

wf = filehandle()
duration = get_duration()
stream = initialize_stream()

app = QApplication(sys.argv)
ex = Example()

sample_rate = 44100

sys.exit(app.exec_())
