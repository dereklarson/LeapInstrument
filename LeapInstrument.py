#!/usr/bin/python
################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time, math
import cPickle as cp
import dSound as dS
from InstrDisplay import InstrDisplay
from Theremin import Theremin


class SampleListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"
        # Instantiate our Theremin
        self.instrument = Theremin(width=1, bitrate=44100)
        self.display = InstrDisplay([640, 480], 'droid', 64)

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        # Shut off everything
        self.instrument.stop_stream()
        self.display.clean()
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        fps = frame.current_frames_per_second
        # Check buffer size for debugging
        d_len = self.instrument.check_data()
        if frame.id % 50 == 0:
            print "FPS: %f, fingers: %d, data_length: %d" % (
                fps, len(frame.fingers), d_len)

        # Improve performance a little by ignoring some frames
        if frame.id % 5 == 0:
            for hand in frame.hands:
                if hand.is_left:
                    # LH height controls the volume
                    self.instrument.set_volume(hand.palm_position[1])
                else:
                    # We use RH roll to mix between our two tones
                    roll = hand.palm_normal.roll
                    w1 = abs(math.cos(roll))
                    w2 = abs(math.sin(roll))

                    # The RH index finger controls pitch
                    for finger in hand.fingers:
                        if finger.type() == finger.TYPE_INDEX:
                            freq = finger.bone(3).next_joint[1]
                            self.instrument.mod_tones(freq, [w1, w2])
                            self.display.draw_all(self.instrument.volume, freq, w1)

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
