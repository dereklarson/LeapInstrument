"""
This class implements a Theremin for use with the Leap Motion controller.
"""


import math, time, array, os
import numpy as np
import cPickle as cp
import pyaudio as PA
import dSound as dS

NWL = 10
os.environ['PULSE_LATENCY_MSEC'] = '200'

class Theremin(object):
    def __init__(self, width=1, bitrate=44100, start=True):
        self.stream_data = None
        self.bitrate = bitrate
        self.width = width
        self.volume = 0.3
        self.c_tones = dS.make_tones([dS.sine, dS.sawtooth],
                [200., 200.], [20., 1.])
        self.sig = self.create_signal(self.c_tones, NWL)
        self.c_sound = self.conv_buffer(self.volume * self.sig)
        self.init_stream_data()
        if start:
            self.stream, self.pa = self.init_stream()

    def init_stream(self, frames_per_buffer=128):
        """Intialize pyaudio stream with callback mode"""
        print "PA stream initiated"
        _pa = PA.PyAudio()

        # callback function repeatedly pulls frame_count frames to play
        def callback(in_data, frame_count, time_info, status):
            data = self.get_data(frame_count)
            return (data, PA.paContinue)
        
        # Open the stream using callback style play
        _stream = _pa.open(format=_pa.get_format_from_width(self.width),
                    channels=1, rate=self.bitrate, output=True,
                    frames_per_buffer=frames_per_buffer,
                    stream_callback=callback)

        return _stream, _pa

    def stop_stream(self):
        self.stream.close()
        self.pa.terminate()
        print "PA stream terminated"

    def get_data(self, frame_count):
        """Supplies audio data to the callback routine"""
        ret = self.stream_data[:frame_count]
        self.stream_data = self.stream_data[frame_count:]
        if len(self.stream_data) < frame_count:
            self.stream_data += self.c_sound
        return ret

    def check_data(self):
        return len(self.stream_data)

    def init_stream_data(self):
        print "Initialized stream data"
        if self.width == 1:
#           self.stream_data = cp.load(open("init_sample"))
            self.stream_data = self.c_sound
        elif self.width == 2:
            self.stream_data = array.array('h')
        elif self.width == 4:
            self.stream_data = array.array('l')

    def mod_tones(self, freq, wt):
        """Alters the frequency and wafeform mix of the tone list"""
        for i in range(len(self.c_tones)):
            self.c_tones[i]['wt'] = wt[i]
            self.c_tones[i]['freq'] = freq
        self.sig = self.create_signal(self.c_tones, NWL)
        self.c_sound = self.conv_buffer(self.volume * self.sig)

    def set_volume(self, h):
        self.volume = max(0., min(1., (h - 50.) / 300.))
        self.c_sound = self.conv_buffer(self.volume * self.sig)

    def create_signal(self, tone_list, length):
        """Makes the analog signal from your tone list. 'length' is given
            in # of wavelengths (avoids clipping)
        """
        num_frame = length * self.bitrate / tone_list[0]['freq']
        p0 = num_frame - int(num_frame)
        num_frame = int(num_frame)
        signal = np.zeros((num_frame,))
        weight = 0

        for tone in tone_list:
            ffreq = self.bitrate / tone['freq']
            arg = np.arange(num_frame) + (tone['phase']) * ffreq
            tone['phase'] = ((arg[-1] + 1) % ffreq) / ffreq
            signal += tone['wt'] * tone['func'](arg, 2 * math.pi / ffreq)
            weight += tone['wt']
            
        signal /= weight
        return signal

    def conv_buffer(self, signal):
        """Takes in the analog signal and converts it to a buffer
            appropriate for playback with the pyaudio stream"""
        if self.width == 1:
            sd = ''
            for x in range(len(signal)):
                sd += chr(int(signal[x]*127+128))
        elif self.width == 2:
            sd = array.array('h')
            for x in range(len(signal)):
                val = int(signal[x]*32767)
                sd.append(val)
        elif self.width == 4:
            sd = array.array('l')
            for x in range(len(signal)):
                val = int(signal[x]*(1 << 30 - 1))
                sd.append(val)
        return sd
