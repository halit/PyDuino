from PyQt4 import QtCore
from PyQt4 import QtGui
from PyDuino import Ui_PyDuino

import sys, arduino

class readDigital(QtCore.QThread):
    statusReady = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def setUp(self, pin, arduino):
        self.pin = pin
        self.arduino = arduino

    def run(self):
        self.readStatus = self.arduino.getState(int(self.pin))

        if self.readStatus == 1:
            self.statusReady.emit("1")
        if self.readStatus == 0:
            self.statusReady.emit("0")

class MainWindow(QtGui.QMainWindow, Ui_PyDuino):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.statusBar().showMessage(unicode("Connection Established\n"))
        self.arduino = arduino.Arduino("/dev/ttyACM0")

        self.readStatus = 0
        self.readStatusPin = 0

        self.pind = 0
        self.pina = 0

    @QtCore.pyqtSignature("bool")
    def on_digitalWriteButton_clicked(self):
        statuspin = str(self.digitalWriteComboBox.currentText())
        statuspin = statuspin.split(" ")

        self.pind = statuspin[1]
        pinstatus = int(self.digitalWriteStatus.currentText())

        if pinstatus == 1:
            self.arduino.setHigh(self.pind)
        if pinstatus == 0:
            self.arduino.setLow(self.pind)
        self.statusBar().showMessage(unicode("Pin: " + self.pind + " Now " + str(pinstatus) + " \n"))

    def on_readButton_clicked(self):
        statuspin = str(self.readComboBox.currentText())

        if "D" in statuspin:
            pindigital = statuspin.split(" ")

            self.pind = pindigital[1]
            self.statusBar().showMessage(unicode("Reading Digital " + self.pind + ". Pin \n"))
            self.digital = readDigital(self)
            self.digital.setUp(self.pind, self.arduino)
            self.digital.statusReady.connect(self.readLcdNumber.display)
            self.digital.start()

            #if self.arduino.getState(int(self.pind)) == 1:
            #    self.pind = self.arduino.getState(int(self.pind))

            #if self.arduino.getState(int(self.pind)) == True:
            #    self.readLcdNumber.display("1")
            #else:
            #    self.readLcdNumber.display("0")

        if "A" in statuspin:

            _pina = statuspin.split(" ")

            self.pina = _pina[1]
            self.statusBar().showMessage(unicode("Reading Analog " + self.pina + ". Pin \n"))

            #while(self.arduino.getState()):
            #    self.pind = self.arduino.getState(self.pind)
            #    self.readLcdNumber.display("321")

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())