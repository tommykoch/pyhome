from time import time, gmtime, strftime, sleep
import os, sys, json, sh
# broken on raspberrypi .-/
# from playsound import playsound
import RPi.GPIO as io
import elro
from sensor import PIRSensor
from config import (ALARM_RED_LED_PIN, ALARM_GREEN_LED_PIN,
                    ALARM_FILE, ALARM_SWITCH, ALARM_SOUND,
                    SENSOR_WAIT, ELRO_KEY, ELRO_PIN)


class  AlarmService(object):

    def __init__(self,
                 switch=ALARM_SWITCH,
                 green_pin=ALARM_GREEN_LED_PIN,
                 red_pin=ALARM_RED_LED_PIN,
                 state_file=ALARM_FILE):
        # ELRO
        devices = { 'A': 1, 'B': 2, 'C': 4, 'D': 8, 'E':16 }
        self.device = devices.get(switch, 0)
        self.green_pin = green_pin
        self.red_pin = red_pin
        self.state_file = state_file
        self.active = True
        self.changed = None  #  date of last (detected) state change

    def setup(self):
        io.setmode(io.BCM)
        io.setwarnings(False)
        io.setup(self.red_pin, io.OUT)
        io.setup(self.green_pin, io.OUT)

    def teardown(self):
        io.cleanup()

    def is_active(self):
        return self.active

    def trigger(self, pause=3):
        """external alarm trigger"""
        # enable lamp
        if self.device:
            self.set_switch()
        # blink
        self.blink(red=True)
        # sound
	self.playsound()
        # disable for short period
        self.set_active(False, False, True)
        # Pause between next check
        sleep(pause)
        self.set_active(True, True, True)

    def playsound(self):
        # play sound - using sox
        if ALARM_SOUND:
            soundfile = os.path.abspath(ALARM_SOUND)
            if os.path.exists(soundfile):
                sh.play(soundfile)

    def save(self, enable=False, disable=False):
        """write new status to file
        reset enable/disable command (unless args given)"""
        data = {}
        data['active'] = self.active
        data['enable'] = enable
        data['disable'] = disable
        with open(self.state_file, 'w') as outfile:
            json.dump(data, outfile)

    def load(self):
        """load  enable/disable command from file - ignore status"""
        enable = disable =  False
        if not os.path.exists(self.state_file):
            return enable, disable
        with open(self.state_file) as json_file:
            data = json.load(json_file)
            enable, disable = data['enable'], data['disable']
        return enable, disable

    def check(self):
        """check for new command start/stop
        """
        # read status file with 3 states
        # alarm_isactive, alarm_enable, alarm_disable
        enable, disable = self.load()
        if not (enable or disable):
            # nothing to do
            return
        if enable and disable:
            print "invalid command: enable and disable"
            # reset commands
            self.save()
            return

        assert (enable!=disable), "invalid command"
        if enable != self.active:
            self.changed = time()
            self.set_active(enable)
        else:
            # reset commands
            self.save()
        return enable

    def set_active(self, enable=True, blink=False, verbose=True):
        self.active = enable
        if verbose:
            print("Anlage ist " + ("aktiv." if enable else "inaktiv."))
        if blink:
            self.blink(enable)
        # io.setup(led_pin, io.OUT)
        io.output(ALARM_GREEN_LED_PIN, enable)
        # reset lamp (i.e. turn off)
        #if self.device:
        #    self.set_switch(False)
        # persist status
        self.save()

    def blink(self, red=False, anzahl=3, period=0.4):
        if red:
            led_pin = self.red_pin
        else:
            led_pin = self.green_pin
        led_on = True
        i = 0
        io.setup(led_pin, io.OUT)
        print "verwende fuer blink LED GPIO pin#",led_pin
        try:
            while (i<anzahl*2):
                print("schalte "+ ("AN" if led_on else "AUS"))
                io.output(led_pin, led_on)
                sleep(period)
                led_on = not led_on
                i+=1
        except Exception,e:
            print "Error:",e

    def set_switch(self, on=True):
        # from elro import  RemoteSwitch
        if not self.device:
            return False
        print("turn device#%d to '%s'" % (self.device,
                                          "on" if on else "off"))
        device = elro.RemoteSwitch(self.device,
                                   key=ELRO_KEY,
                                   pin=ELRO_PIN)
        if on:
            device.switchOn()
        else:
            device.switchOff()
        return True


if __name__ == "__main__":
    default_wait = SENSOR_WAIT
    # create  PIR sensor
    sensor = PIRSensor()
    # create alarm service
    alarm = AlarmService()
    alarm.setup()
    try:
        print "Starting Alarm service ..."
        alarm.set_active(enable=True, blink=True, verbose=True)
        #loop forever, well until Ctrl+C
        while(True):
            if alarm.is_active() and sensor.motion_detected():
                motiondetected = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                # trigger alarm service
                alarm.trigger()
            # check for new alarm commands
            print("check for new alarm commands")
            alarm.check()
            sleep(default_wait)
    #Ctrl+C
    except KeyboardInterrupt:
        print "Cancelled"
    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    finally:
        alarm.teardown()

