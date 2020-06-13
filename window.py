import sys
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QToolTip, QWidget
#from PyQt5.QtGui import QFont, Qt
from PyQt5.QtCore import QTime, QTimer
from bpm import *
from detector import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class UI(QWidget):
    timer_period = int(round(1000 / (180 / 60) / 16))  # 180bpm / 16
    
    
    def __init__(self):
        super().__init__()
        self.audio_analyser = AudioAnalyzer()

        self.change_program = False
        self.auto_prog = False
        self.timer = QTimer()
        self.bt1 = QPushButton("Auto Start OFF", self)
        self.bt2 = QPushButton("Auto Start OFF", self)
        self.bt3 = QPushButton("Beat", self)
        self.bt4 = QPushButton("BPM", self)
        self.vb = QVBoxLayout()
        self.setup()
        

    def setup(self):
        """Window Definitions"""
        self.setGeometry(700, 450, 350, 200)
        self.setWindowTitle("BeatDetector")
        self.button1()
        self.button2()
        self.button3()
        self.button4()
        self.v_box()
        # adding action to timer 
        self.timer.timeout.connect(self.clock) 
        # update the timer every tenth second 
        self.timer.start(100) 
        self.show()
        

    def button1(self):
        self.bt1.setToolTip('Start audio Tracking')
        self.bt1.setFont(QFont('Arial', 15, QFont.Bold))
        self.bt1.setStyleSheet("background-color: red")
        self.bt1.clicked.connect(self.on_auto_start_button_clicked)
        

    def button2(self):
        self.bt2.setFont(QFont('Arial', 15, QFont.Bold))
       

    def button3(self):
        self.bt3.setFont(QFont('Arial', 15, QFont.Bold))
       

    def button4(self):
        self.bt4.setFont(QFont('Arial', 15, QFont.Bold))
        

    def v_box(self):
        self.vb.addWidget(self.bt1)
        self.vb.addWidget(self.bt2)
        self.vb.addWidget(self.bt3)
        self.vb.addWidget(self.bt4)
        self.setLayout(self.vb)
        

    def on_auto_start_button_clicked(self):
        self.auto_prog = not self.auto_prog
        if self.auto_prog:
            self.change_program = True
        self.change_auto_start_state(self.auto_prog)

    def change_auto_start_state(self, enabled):
        if enabled:
            self.bt1.setText("Auto Start ON")
            self.bt1.setStyleSheet("background-color: green")
        else:
            self.bt1.setText("Auto Start OFF")
            self.bt1.setStyleSheet("background-color: red")

    
            
    def clock(self):
        print(300)
        if self.auto_prog == True:
            self.audio_analyser.analyze_audio()
            print(400)
        

