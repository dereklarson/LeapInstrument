import math
import numpy as np

def sawtooth(x, omega):
    tau_i = omega / (2 * math.pi)
    return 0.4 * (x * tau_i - np.floor(0.5 + x * tau_i))

def sine(x, omega):
    return np.sin(x * omega)

def make_tones(func_list, freq_list, wt_list):
    tone_list = []
    for i in range(len(func_list)):
        tone_list.append({'func': func_list[i], 'freq': freq_list[i],
                            'wt': wt_list[i], 'phase': 0, 'vol': 1})
    return tone_list

def chord1351(func, base):
    return [{'func': func, 'freq': base * 1.00, 'wt': 1, 'phase': 0, 'vol': 1},
            {'func': func, 'freq': base * 1.26, 'wt': 1, 'phase': 0, 'vol': 1},
            {'func': func, 'freq': base * 1.50, 'wt': 1, 'phase': 0, 'vol': 1},
            {'func': func, 'freq': base * 2.00, 'wt': 1, 'phase': 0, 'vol': 1}]
