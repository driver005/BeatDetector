import sys
import numpy
from time import perf_counter
from PyQt5 import QtGui
from detector import *
from window import *
    

"""Main Program"""

    

if __name__ == "__main__":
    input_recorder = InputRecorder()
    app = QApplication(sys.argv)
    input_recorder.start()
    window = UI()
    window.show()

    

    
    sys.exit(app.exec_())