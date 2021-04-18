# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\timedHelper.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import random
import cv2

# supported file extensions
# [".jpg", ".jpeg", ".png", ".gif"]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 640)
        # MainWindow.setStyleSheet("background-color: rgb(150, 150, 150);")
        MainWindow.setLocale(
            QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom)
        )
        MainWindow.setAnimated(True)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # My vars----------------------------------------------
        self.wndHandle = MainWindow
        self.timer_ = 60
        self.counter_ = self.timer_
        self.dir_ = "C:/"
        self.imgList_ = []

        self.lbl = QtWidgets.QLabel(self.centralwidget)
        self.lbl.setGeometry(QtCore.QRect(0, 0, 480, 640))

        # -----------------------------------------------------
        self.res_ = (480, 640)
        self.widRect_ = QtCore.QRect()

        self.spinBoxHidden = True
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(410, 0, 71, 31))

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.spinBox.setFont(font)
        self.spinBox.setStyleSheet('font: 24pt "Calibri";')
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setValue(self.counter_)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(600)
        self.spinBox.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.spinBox.show()

        self.showTimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.showTimeLabel.setGeometry(QtCore.QRect(410, 0, 71, 31))
        self.showTimeLabel.setFont(font)
        self.showTimeLabel.setStyleSheet('font: 24pt "Calibri";')
        self.showTimeLabel.setObjectName("showTimeLbl")
        self.showTimeLabel.setText(str(self.counter_))
        self.showTimeLabel.hide()
        self.showTimeLabel.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        # -----------------------------------------------------

        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.toolBar.setFont(font)
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionPath = QtWidgets.QAction(MainWindow)
        self.actionPath.setObjectName("actionPath")
        self.actionStart_Stop = QtWidgets.QAction(MainWindow)
        self.actionStart_Stop.setObjectName("actionStart_Stop")

        self.actionSetTime = QtWidgets.QAction(MainWindow)
        self.actionPath.setObjectName("setTimeEnable")

        self.toolBar.addAction(self.actionPath)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.actionStart_Stop)
        self.toolBar.addSeparator()

        self.toolBar.addAction(self.actionSetTime)
        self.toolBar.addSeparator()

        # additional logic--------------------------------------
        self.is_running_ = False
        self.clock = QTimer()
        self.clock.timeout.connect(self.onTimeout)
        self.clock.start(self.timer_)
        self.clock.setInterval((1000))

        self.actionPath.triggered.connect(self.browseFolder)
        self.actionStart_Stop.triggered.connect(self.start)
        self.actionSetTime.triggered.connect(self.enableSpinBox)

        self.spinBox.valueChanged.connect(self.setTime)

        self.checkConfig()
        # ------------------------------------------------------

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def computeWidRect(self):
        width = self.wndHandle.geometry().width()
        height = self.wndHandle.geometry().height()
        xpos = (width - 71, width)
        ypos = (0, 31)
        return xpos, ypos

    def checkConfig(self):
        exists = False

        if os.path.isfile("folders.config"):
            print("Found folders.config, will load images from there")
            with open("folders.config") as f:
                content = f.readlines()
            self.dir_ = content[0]
            if self.dir_ == None:
                self.dir_ = "C:/"
            exists = True
            self.imgList_ = [
                self.dir_ + "/" + f
                for f in os.listdir(self.dir_)
                if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")
            ]
        else:
            print("File folders.config doesnt exist. Will create.")
        return exists

    def enableSpinBox(self):
        self.is_running_ = False
        if not self.spinBoxHidden:
            self.spinBox.show()
            self.showTimeLabel.hide()
        else:
            self.showTimeLabel.setText(str(self.timer_))
            self.showTimeLabel.show()
            self.spinBox.hide()
        self.spinBoxHidden = not self.spinBoxHidden

    def browseFolder(self):
        self.dir_ = QFileDialog.getExistingDirectory(
            None, "Select a folder:", "C:\\", QFileDialog.ShowDirsOnly
        )
        f = open("folders.config", "w")
        f.write(self.dir_)
        f.close()

        if self.dir_ == "" or self.dir_ == None:
            self.dir_ = "C:/"
        else:
            self.imgList_ = [
                self.dir_ + "/" + f
                for f in os.listdir(self.dir_)
                if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")
            ]

        self.is_running_ = False

        return

    def start(self):
        self.counter_ = self.timer_
        self.is_running_ = not self.is_running_
        if self.is_running_ == True:

            if len(self.imgList_) == 0:
                print("couldnt find image list")
                self.is_running_ = False
            else:
                self.showTimeLabel.setText(str(self.timer_))
                print("drawing at start")
                randomVal = random.randint(0, len(self.imgList_) - 1)
                self.draw(randomVal)

        return

    def resize(self, w, h):
        self.wndHandle.resize(w, h)
        self.lbl.setGeometry(QtCore.QRect(0, 0, w, h))
        xpos, ypos = self.computeWidRect()
        self.spinBox.setGeometry(QtCore.QRect(xpos[0], ypos[0], xpos[1], ypos[1]))
        self.showTimeLabel.setGeometry(QtCore.QRect(xpos[0], ypos[0], xpos[1], ypos[1]))

    def setTime(self):
        if self.is_running_:
            self.is_running_ = False
        self.timer_ = self.spinBox.value()
        self.counter_ = self.timer_
        self.showTimeLabel.setText(str(self.counter_))

    def onTimeout(self):

        if len(self.imgList_) > 0:
            if self.is_running_ == True:
                if self.counter_ <= 0:
                    randomVal = random.randint(0, len(self.imgList_) - 1)
                    self.draw(randomVal)
                    self.counter_ = self.timer_
                self.showTimeLabel.setText(str(self.counter_))
                self.counter_ = self.counter_ - 1
        return

    def draw(self, randomVal):
        cvImg = cv2.imread(self.imgList_[randomVal])
        height, width, _ = cvImg.shape
        cvImg = cv2.cvtColor(cvImg, cv2.COLOR_RGBA2BGR)
        bytesPerLine = 3 * width
        qImg = QImage(
            cvImg.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888
        )
        self.resize(width, height)
        self.lbl.setPixmap(QtGui.QPixmap.fromImage(qImg))

        return

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionPath.setText(_translate("MainWindow", "Path"))
        self.actionPath.setToolTip(
            _translate(
                "MainWindow", "Path to your image folder, shortcut: Ctrl+Shift+F"
            )
        )
        self.actionPath.setShortcut(_translate("MainWindow", "Ctrl+Shift+F"))
        self.actionStart_Stop.setText(_translate("MainWindow", "Start/Stop"))
        self.actionStart_Stop.setToolTip(
            _translate("MainWindow", "Start the Timed Drawing, shortcut: Ctrl+Space")
        )
        self.actionStart_Stop.setShortcut(_translate("MainWindow", "Ctrl+Space"))
        self.actionSetTime.setText(_translate("MainWindow", "Set Time"))
        self.actionSetTime.setToolTip(
            _translate("MainWindow", "Enable Set Time spinbox")
        )
        self.actionSetTime.setShortcut(_translate("MainWindow", "Ctrl+T"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setWindowFlags(
        QtCore.Qt.Window
        | QtCore.Qt.CustomizeWindowHint
        | QtCore.Qt.WindowTitleHint
        | QtCore.Qt.WindowCloseButtonHint
        | QtCore.Qt.WindowStaysOnTopHint
    )
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
