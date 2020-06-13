import matplotlib
import numpy as np
import pyaudio
import threading
matplotlib.use('TkAgg')  # <-- THIS MAKES IT FAST!



class InputRecorder:

    def __init__(self):
        self.CHUNK = 1024 * 4
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.BUFFERSIZE = 2 ** 10
        self.secToRecord = 0.1
        self.multithreads = True
        self.audio_detection = False
        self.stream  = pyaudio.PyAudio()

        self.bit_depth = int(self.RATE / self.BUFFERSIZE * self.secToRecord)
        if self.bit_depth == 0:
            self.bit_depth = 1
        self.samples_frequency = int(self.BUFFERSIZE * self.bit_depth)
        self.sec_per_point = 1.0 / self.RATE

    def setup(self):
         
        self.stream.open(
                    format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=self.CHUNK
        )
        print(type(self.stream))
        self.audio = np.empty((self.samples_frequency), dtype=np.int16)

    def read_audio(self):
        """Liest die Daten aus dem Audiobuffer (Musik) und schreibt es in ein 2D Array"""
        audio_buffer = self.stream.read(self.BUFFERSIZE)
        return np.frombuffer(audio_buffer, dtype=np.int16)

    def record_audio(self):
        """Ersetzt die 1, 2, 3, 4 1024 Element von audio (Z.38) mit den gelesen Werten aus dem Audiobuffer (Musik)"""
        while self.multithreads:
            for i in range(self.bit_depth):
                self.audio[i * self.BUFFERSIZE:(i + 1) * self.BUFFERSIZE] = self.read_audio()
            self.audio_detection = True

    def start(self):
        threading._start_new_thread(self.record_audio)
        #self.p1.start()

    def close(self):
        self.multithreads = False
        self.p.close(self.stream)

    def fft(self, data=None, trim_by=2, log_scale=False, div_by=100):
        if not data:
            data = self.audio.flatten()
        left, right = np.split(np.abs(np.fft.fft(data)), 2)
        ys = np.add(left, right[::-1])
        if log_scale:
            ys = np.multiply(np.log10(ys), 20)
        xs = np.arange(self.BUFFERSIZE / 2, dtype=float)
        if trim_by:
            i = int((self.BUFFERSIZE / 2) / trim_by)
            ys = ys[:i]
            xs = xs[:i] * self.RATE / self.BUFFERSIZE
        if div_by:
            ys = ys / float(div_by)
        return xs, ys
