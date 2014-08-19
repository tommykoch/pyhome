from time import time, gmtime, strftime, sleep
import RPi.GPIO as io
import os, sys

default_pin = 18
default_state = 0
default_wait  = 2  # 2 seconds polling intervall
delta_time = 5     # 5 seconds to wait until next motion
motionfile = "motion.txt"

class  GPIOSensor(object):

    def __init__(self, pin=default_pin, state=default_state):
        self.pin = pin
        self.state = default_state
        self.changed = None  #  date of last (detected) state change
        io.setmode(io.BCM)
        io.setup(self.pin, io.IN)

    def check(self):
        """check for new state"""
        new_state = io.input(self.pin)
        if new_state != self.state:
            self.changed = time()
            self.state = new_state
        return new_state


class PIRSensor(GPIOSensor):

    def __init__(self, pin=default_pin, state=default_state):
        super(PIRSensor, self).__init__(pin, state)
        self.last_check = None

    def motion_detected(self):
        """check for motion detected"""
        now = time()
        if (self.last_check is None or self.state is None 
            or now-self.last_check > delta_time):
            last_check = now
            last_state = self.state
            new_state = self.check()
         
            if last_state and new_state:
                # two events "High"
                motion = True
                self.state = False # reset
            else:
                motion = False
        return motion


# TODO: Thread to monitor sensor
# write state = last motion into file

def touch(fname=motionfile, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

if __name__ == "__main__":
    # create  PIR sensor
    sensor = PIRSensor()
    try:
        print "Starting PIR sensor..."
        #loop forever, well until Ctrl+C
        while(True):
            if sensor.motion_detected():
                motiondetected = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                print "\nmotiondetected: %s" % motiondetected
                touch()  # simply update motion file's timestamp
            sleep(default_wait)
    #Ctrl+C
    except KeyboardInterrupt:
        print "Cancelled"
    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
