#!/usr/bin/env python

from PySide.QtGui import QApplication, QVBoxLayout, \
                         QDial, QPushButton, QGroupBox
import sys
import threading


sensor = None


class ActualFakeSensor(object):
    def __init__(self, callback=None):
        self.callback = callback

        self.app = QApplication(sys.argv)

        self.layout = QVBoxLayout()

        self.dial = QDial()
        self.dial.valueChanged.connect(self.dial_callback)
        self.dial.setNotchesVisible(True)
        self.dial.setWrapping(True)
        self.layout.addWidget(self.dial)

        self.quit = QPushButton('Quit')
        self.quit.clicked.connect(self.app.quit)
        self.layout.addWidget(self.quit)

        self.group = QGroupBox('Fake Sensor')
        self.group.setLayout(self.layout)

    def dial_callback(self, value):
        if self.callback:
            self.callback(self.value())

    def register_callback(self, callback):
        self.callback = callback

    def value(self):
        return self.dial.value()

    def set_value(self, value):
        self.dial.setValue(value)

    def run(self):
        self.group.show()
        self.app.exec_()


class FakeSensor(object):
    def __init__(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        self.sensor = ActualFakeSensor()
        self.sensor.run()

    @property
    def value(self):
        return self.sensor.value()

    def register_callback(self, callback):
        return self.sensor.register_callback(callback)


if __name__ == '__main__':
    sensor = FakeSensor()

    from time import sleep
    while True:
        print('x')
        sleep(1)
