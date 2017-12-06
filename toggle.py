#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import sys
from PyQt5.QtCore import Qt


from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QFrame, QApplication, QLCDNumber, QSlider,
                             QVBoxLayout)

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

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

    return stream

def get_duration(wf):
    frames = wf.getnframes()
    rate = wf.getframerate()
    duration = frames / float(rate)
    return duration


def toggle_stream():
    if stream.is_active():
        stream.stop_stream()
    else:
        stream.start_stream()

"""
ZetCode PyQt5 tutorial

In this example, we create three toggle buttons.
They will control the background color of a
QFrame.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        pause_play_button = QPushButton('Pause Play', self)
        pause_play_button.setCheckable(True)
        pause_play_button.move(10, 10)

        pause_play_button.clicked[bool].connect(self.handleClicks)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Toggle button')
        self.show()

    def handleClicks(self, pressed):
        global stream

        source = self.sender()

        if source.text() == "Pause Play":
            toggle_stream()


app = QApplication(sys.argv)
ex = Example()

wf = filehandle()

duration = get_duration(wf)

stream = initialize_stream()

sys.exit(app.exec_())
