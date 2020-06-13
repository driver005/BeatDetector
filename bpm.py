import numpy
from window import *
from detector import *
from time import perf_counter
from PyQt5.QtGui import QFont

class AudioAnalyzer:
    low_freq_avg_list: list
    colors_list: list
    bpm_list: list
    curr_time: float
    prev_beat: float
    colors_idx: int
    

    def __init__(self):
        self.input_recorder = InputRecorder()
        #self.my_Ui = UI()
        self.curr_time = perf_counter()
        self.colors_list = ["red", "blue", "green"]
        self.colors_idx = 0
        self.bpm_list = []
        self.low_freq_avg_list = []

    def analyze_audio(self):
        print(200)
        if not self.input_recorder.audio_detection:
            return

        # get x and y values from FFT
        xs, ys = self.input_recorder.fft()

        # calculate average for all frequency ranges
        y_avg = numpy.mean(ys)

        # calculate low frequency average
        low_freq = [ys[i] for i in range(len(xs)) if xs[i] < 1000]
        low_freq_avg = numpy.mean(low_freq)

        self.low_freq_avg_list.append(low_freq_avg)
        cumulative_avg = numpy.mean(self.low_freq_avg_list)

        bass = low_freq[:int(len(low_freq) / 2)]
        bass_avg = numpy.mean(bass)
        # print("bass: {:.2f} vs cumulative: {:.2f}".format(bass_avg, cumulative_avg))

        # check if there is a beat
        # song is pretty uniform across all frequencies
        if (y_avg > 10 and (bass_avg > cumulative_avg * 1.5 or
                            (low_freq_avg < y_avg * 1.2 and bass_avg > cumulative_avg))):

            # print(curr_time - prev_beat)
            if self.curr_time - self.prev_beat > 60 / 180:  # 180 BPM max
                # print("beat")
                # change the button color
                self.colors_idx += 1
                self.my_Ui.bt4.setStyleSheet("background-color: {:s}".format(self.colors_list[
                    self.colors_idx % len(self.colors_list)]), 15, QFont.Bold)

                # change the button text
                bpm = int(60 / (self.curr_time - self.prev_beat))
                if len(self.bpm_list) < 4:
                    if bpm > 60:
                        self.bpm_list.append(bpm)
                else:
                    bpm_avg = int(numpy.mean(self.bpm_list))
                    if abs(bpm_avg - bpm) < 35:
                        self.bpm_list.append(bpm)
                    self.my_Ui.bt4.setText("BPM: {:d}".format(bpm_avg), 15, QFont.Bold)

                # reset the timer
                self.prev_beat = self.curr_time

        # shorten the cumulative list to account for changes in dynamics
        if len(self.low_freq_avg_list) > 50:
            self.low_freq_avg_list = self.low_freq_avg_list[25:]
            # print("REFRESH!!")

        # keep two 8-counts of BPMs so we can maybe catch tempo changes
        if len(self.bpm_list) > 24:
            self.bpm_list = self.bpm_list[8:]

        # reset song data if the song has stopped
        if y_avg < 10:
            bpm_list = []
            low_freq_avg_list = []
            self.my_Ui.bt4.setText("BPM", 15, QFont.Bold)
            # print("new song")

        self.input_recorder.newAudio = False
        print(1)



