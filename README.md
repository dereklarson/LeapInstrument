LeapInstrument - Using the Leap Motion controller to play music
============

Dependencies:  pyaudio, pygame, numpy/scipy, in addition to a Leap setup.

Run `python LeapInstrument.py` with your controller plugged in. The only
'instrument' is a simple Theremin-like implementation. Your left hand
(y-axis) controls the volume and your right hand controls the pitch
(y-axis) and waveform mix (roll). With your right hand surface normal
aligned with the y-axis, it produces a mostly sine wave sound. As you roll
the right hand, it adds more sawtooth wave weight.
