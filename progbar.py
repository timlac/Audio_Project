import time
import pyaudio
import wave
from PyQt5 import QtCore
from PyQt5 import QtWidgets


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

class ExcelCheck(QtCore.QThread):
    updated = QtCore.pyqtSignal(int)
    running = False

    def __init__(self, parent=None):
        super(ExcelCheck, self).__init__(parent)
        self.progPercent = 0
        self.running = True

    def run(self):
        while self.running:
            self.progPercent += 1
            self.progPercent %= duration
            self.updated.emit(int(self.progPercent))
            time.sleep(0.01)

    def stop(self):
        self.running = False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.btn_active = False

    def startBtnClicked(self):
        self.btnStart.setText('start!')
        self.btn_active = True
        self.tmr = ExcelCheck(self)
        self.tmr.updated.connect(self.updateValue)
        self.tmr.start()

    def updateValue(self, data):
        self.progressBar.setValue(data)

    def exitBtnClicked(self):
        # self.ExcelCheck()
        self.btn_active = False
        self.tmr.stop()
        self.sys.exit()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(446, 207)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(40, 70, 381, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(110, 110, 75, 23))
        self.btnStart.setObjectName("btnStart")
        self.btnStart.clicked.connect(self.startBtnClicked)

        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setGeometry(QtCore.QRect(260, 110, 75, 23))
        self.btnExit.setObjectName("btnExit")
        self.btnExit.clicked.connect(self.exitBtnClicked)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 446, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SCM21"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        self.btnExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()

    wf = filehandle()

    duration = get_duration(wf)

    stream = initialize_stream()

    sys.exit(app.exec_())