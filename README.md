PyHome
======

PyHome consists of a sample web application for remote control and simple monitoring - based on a set of python scripts for home automation. 

The code belongs to the (german) presentation 'HeimAutomatisierung mit Python und RaspberryPi' held at FrOSCon 2014:
https://programm.froscon.de/2014/events/1467.html

Requirements
------------

PyHome requires Python 2.6 or 2.7 and Flask (python web framework) and RPi.GPIO (Python GPIO interface for Raspberry Pi). The Web GUI uses jQuery Mobile (1.4.3) but the minified JS files are included in this repository for convenience.


Installation
------------

It is recommended (though optional) to create a virtual environment (see http://virtualenvwrapper.readthedocs.org/) for this project:

    $ mkvirtualenv pyhome

Next install the required Python dependencies via

    $ pip install -r requirements.txt 

