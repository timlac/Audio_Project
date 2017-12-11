import pyaudio
import wave
import sys
from PyQt5.QtWidgets import (QWidget,
                             QApplication, QPushButton)
import threading
import os

class Worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #flag to pause thread
        self.paused = False

        self.frames = []

        self.supress_warnings = False

        # Explicitly using Lock over RLock since the use of self.paused
        # break reentrancy anyway, and I believe using Lock could allow
        # one thread to pause the worker, while another resumes; haven't
        # checked if Condition imposes additional limitations that would
        # prevent that. In Python 2, use of Lock instead of RLock also
        # boosts performance.
        self.pause_cond = threading.Condition(threading.Lock())

    def get_frames(self):
        return self.frames

    def run(self):
        while True:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                data = stream.read(CHUNK)

                # disk usage warnings
                if not self.supress_warnings:
                    if disk_usage() < warning_disk_space:
                        print("warning, low free disk space, only " + str(disk_usage()) + "b remaining" +
                              "\nPress Record to continue")
                        self.pause()
                        self.supress_warnings = True

                self.frames.append(data)

    def pause(self):
        print("recording paused")
        self.paused = True
        # If in sleep, we acquire immediately, otherwise we wait for thread
        # to release condition. In race, worker will still see self.paused
        # and begin waiting until it's set back to False
        self.pause_cond.acquire()

    #should just resume the thread
    def resume(self):
        print("recording resumed")
        self.paused = False
        # Notify so thread will wake after lock released
        self.pause_cond.notify()
        # Now release the lock
        self.pause_cond.release()


class RecordGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

        # self.background_increment = QThread.

    def initUI(self):

        # record button
        self.pushButton = QPushButton("Record", self)
        self.pushButton.setGeometry(30, 30, 70, 30)
        self.pushButton.setObjectName("recordButton")
        self.pushButton.clicked.connect(self.start_pause)

        # save button
        self.pushButton = QPushButton("Save", self)
        self.pushButton.setGeometry(30, 70, 70, 30)
        self.pushButton.setObjectName("saveButton")
        self.pushButton.clicked.connect(self.save)

        # configure placements in window
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Music Player')
        self.show()

        self.Recorder = Worker()

    def start_pause(self, pressed):
        print("button pushed!")

        if not self.Recorder.is_alive():
            stream.start_stream()
            self.Recorder.start()
        else:
            if not self.Recorder.paused:
                self.Recorder.pause()
                stream.stop_stream()
            else:
                stream.start_stream()
                self.Recorder.resume()

    def save(self):
        if not self.Recorder.paused:
            self.Recorder.pause()
            stream.stop_stream()

        stream.close()
        p.terminate()
        frames = self.Recorder.get_frames()
        self.close()
        save_as_handler(frames)
        sys.exit()

def saveFile(frames, FILENAME):
    waveFile = wave.open(FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def initialize_stream():
    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)
    stream.stop_stream()
    return stream

def disk_usage():
    path = "/usr"

    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    st = os.statvfs(path)
    free_space = st.f_bavail * st.f_frsize

    return free_space

def setFileName():
    FILENAME = input("Save as: ") + str(".wav")
    return FILENAME

def save_as_handler(frames):
    # Confirm overwrite of file
    while True:
        FILENAME = setFileName()

        if os.path.exists(FILENAME):
            # return True
            overwrite = input("Do you want to overwrite an already existing file? Answer: 'yes' or 'no': ")
            if overwrite == "no":
                print("Well, we'll try again: ")
            elif overwrite == "yes":
                saveFile(frames, FILENAME)
                print("Saved as " + FILENAME)
                break
            else:
                print("Wrong answer! Come on dude.")
        else:
            saveFile(frames, FILENAME)
            print("Saved as " + FILENAME)
            break
    return


# warn if less than ** mb free disk space
warning_disk_space = 1000
p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 2
RATE = 44100
WIDTH = 2

stream = initialize_stream()

app = QApplication(sys.argv)
GUI = RecordGUI()
sys.exit(app.exec_())