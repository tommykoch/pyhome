PyHome
======

PyHome consists of a sample web application for remote control and simple monitoring - based on a set of python scripts for home automation. 

The code belongs to the (German) presentation 'HeimAutomatisierung mit Python und RaspberryPi' held at FrOSCon 2014:
https://programm.froscon.de/2014/events/1467.html - see slides (in German) at http://de.slideshare.net/tomykoch/heimautomatisierung-mit-python-und-raspberry-pi

Requirements
------------

You'd need a Raspberry Pi with Raspbian OS and Python. PyHome requires Python 2.6 or 2.7 and Flask (python web framework) and RPi.GPIO (Python GPIO interface for Raspberry Pi). The Web GUI uses jQuery Mobile (1.4.3) but the minified JS files are included in this repository for convenience.


In order to control switches you will need a 433.92 MHz transmitter and 'Elro compatible' switches.
For technical details see http://www.gtkdb.de/index_36_2261.html

Installation
------------

It is recommended (though optional) to create a virtual environment (see http://virtualenvwrapper.readthedocs.org/) for this project:

    $ mkvirtualenv pyhome

Next install the required Python dependencies via

    $ pip install -r requirements.txt 

Usage
-----

If you want to use webcam support you need to install fswebcam:

    $ sudo apt-get install fswebcam

Otherwise set webcam = False in home.py

If you want to use the motion sensor (and have a PIR sensor connected) run

    $ cd web
    $ sudo python sensor.py

to start the sensor (keep this running in a shell).

Finally start the web frontend via

    $ cd web
    $ sudo python home.py 
    $ open http://127.0.0.1:8080/
    

Credits
-------

The script elropi.py for switching Elro devices using Python on Raspberry Pi has been developed by Heiko H: http://pastebin.com/aRipYrZ6


Some icons are from a free icon set by IcoMoon - see http://icomoon.io/#docs or watch this repository on github:
https://github.com/Keyamoon/IcoMoon--limited-
