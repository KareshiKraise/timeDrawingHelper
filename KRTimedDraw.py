# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
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
import cv2 
import random


#supported file extensions
#exts = [".jpg", ".jpeg", ".png"]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(617, 742)

        self.counter_ = 0

        self.imgList_ = []

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(10, 0, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(600)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 0, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(550, -10, 101, 41))
        

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.timer_ = 20
        self.dir_ = ""

        self.is_running_ = False;
        self.currentImage_ = ""

        self.pic = QtWidgets.QLabel(self.centralwidget)
        self.pic.setGeometry(QtCore.QRect(0, 30, 620, 710))
        self.pic.setObjectName("ImageArea")
        
        self.pic.setScaledContents(True)
        self.pic.show()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 617, 21))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.actionSet_timer = QtWidgets.QAction(MainWindow)
        self.actionSet_timer.setObjectName("actionSet_timer")
        self.actionSet_images_folder = QtWidgets.QAction(MainWindow)
        self.actionSet_images_folder.setObjectName("actionSet_images_folder")
        self.menuSettings.addAction(self.actionSet_images_folder)
        self.menubar.addAction(self.menuSettings.menuAction())

        self.spinBox.valueChanged.connect(self.setTimer)
        self.actionSet_images_folder.triggered.connect(self.browseFolders)

        self.clock = QTimer()
        self.clock.timeout.connect(self.onTimeout)        
        self.clock.start(self.timer_)
        self.clock.setInterval((1000))        

        self.pushButton.clicked.connect(self.start)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def start(self):
        
        self.counter_ = 0        

        if self.is_running_ == False:
           if len(self.imgList_) == 0 or self.dir_ == "" or self.dir_ == None:    
               self.pic.setText("No folder selected")    
           else:
               randomVal = random.randint(0, len(self.imgList_)-1)  
               try:              
                   self.pic.setPixmap(QtGui.QPixmap.fromImage(self.loadImage(self.imgList_[randomVal])))
                   self.pic.setScaledContents(True)
                   self.pic.show()
               except IndexError:
                   print("random val was: ", randomVal)
                   print("length, ", len(self.imgList_))

        self.is_running_ = not self.is_running_

    def onTimeout(self):

        if len(self.imgList_) == 0:    
            self.pic.setText("No folder selected")          
        
        else:

            if self.is_running_ == True:           
                if self.counter_ >= self.timer_:
                    #draw next image on screen
                    randomVal = random.randint(0, len(self.imgList_)-1)  
                    try:                                        
                        print(f"current image: {self.imgList_[randomVal]}")                        
                        self.pic.setPixmap(QtGui.QPixmap.fromImage(self.loadImage(self.imgList_[randomVal])))
                        self.pic.setScaledContents(True)
                        self.pic.show()
                    except IndexError:
                        print("random val was: ", randomVal)
                        print("length, ", len(self.imgList_))
                        
                    self.counter_ = 0            
                self.label.setText(str(self.counter_))
                self.counter_ += 1
             
    def loadImage(self, path):        
        cvImg = cv2.imread(path)
        height, width, channel = cvImg.shape

        yfactor = 1
        xfactor = 1
        if height > 680:            
            yfactor = 680/height            
        if width > 620:
            xfactor = 620/height

        cv2.resize(cvImg, dsize=(int(height*yfactor), int(width*xfactor)),interpolation=cv2.INTER_CUBIC)
        cvImg = cv2.cvtColor(cvImg, cv2.COLOR_RGBA2BGR)        
        
        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)

        return qImg


    def setTimer(self):
        self.timer_ = self.spinBox.value()  
        self.is_running = False    
        self.counter_ = 0  
        return


    def browseFolders(self):

        self.dir_ = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly) 
        
        if self.dir_ == "" or  self.dir_ == None:
            self.pic.setText("Please Select a Folder")                  
            self.dir_ = "C:/"
        else:
            self.imgList_ = [self.dir_+"/"+f for f in os.listdir(self.dir_) if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")]
            
        self.is_running_ = False
        return

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start/Stop"))
        self.label.setText(_translate("MainWindow", "0"))    
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionSet_timer.setText(_translate("MainWindow", "Set timer"))
        self.actionSet_images_folder.setText(_translate("MainWindow", "Set images folder"))
   

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    MainWindow.setWindowFlags(QtCore.Qt.Window |
        QtCore.Qt.CustomizeWindowHint |
        QtCore.Qt.WindowTitleHint |
        QtCore.Qt.WindowCloseButtonHint |
        QtCore.Qt.WindowStaysOnTopHint)

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
