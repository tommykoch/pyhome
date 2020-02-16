# home configuration
HTTP_PORT = 8000
DEBUG = True

# Temperature Sensor
TEMPERATURE = True

# Alarm
ALARM = True
ALARM_RED_LED_PIN = 23
ALARM_GREEN_LED_PIN = 24
ALARM_FILE = "alarm.json"
ALARM_SWITCH = 'A'  #  Elro

# path to alarm sound file (.mp3)
# see http://soundbible.com/tags-alarm.html for examples
ALARM_SOUND = "sounds/siren-noise.mp3"
# PIR SENSOR
SENSOR = True
SENSOR_FILE = "motion.txt"
SENSOR_PIN = 18
# seconds to wait between two checks for new alarm
SENSOR_WAIT = 2

# ELRO REMOTE SWITCHEs
SWITCH_A = True
SWITCH_B = True
SWITCH_C = True
ELRO_KEY = [1,0,0,0,1]
ELRO_PIN = 17

# enable webcam support
WEBCAM = True
