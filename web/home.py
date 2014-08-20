from flask import Flask, jsonify, request, redirect, url_for
import datetime

app = Flask(__name__)

# config data
elro_key = [1,0,0,0,1]
# change the pin(s) accpording to your wiring
elro_pin =17
# status file for motion detection
motionfile = "motion.txt"
# enable webcam support
webcam = True


@app.route('/')
def index():
    return redirect('/static/home/index.html')


@app.route("/status", methods=["GET"])
def status():
    import os, time
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    details  = { 'temperature':  21.5,  # TODO
                       'time': timeString   # update time
    }
    # read status of PIR sensor
    if os.path.exists(motionfile):
        details['motion'] = time.ctime(os.path.getmtime(motionfile))
    if webcam:
        import sh, os
        timeString = now.strftime("%Y%m%d_%H%M")
        snapshot = "snapshot-%s.jpg" % timeString
        snapshot = os.path.join("static", "webcam", snapshot)
        details['webcam'] = '/'+snapshot
        snapshot = os.path.abspath(snapshot)
        sh.fswebcam("--title", "Home", "--save", snapshot)
    return jsonify(**details)


@app.route("/turn/<switch>", methods=["POST"])
def turn(switch):
    on = request.form['cmd']=="on"
    details  = {}
    if turnSwitch(switch, on):
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        details.update({'time': timeString})
    return jsonify(**details)


def  turnSwitch(switch, on=False):
    from elro import  RemoteSwitch
    devices = { 'A': 1, 'B': 2, 'C': 4, 'D': 8, 'E':16 }
    device=devices.get(switch, 0)
    if not device:
        return False
    # print "turn switch '%s' to '%s' - device#%d"  % (switch, "on" if on else "off", device)
    device = RemoteSwitch(device,
                                             key=elro_key,
                                             pin=elro_pin)
    if on:
        device.switchOn()
    else:
        device.switchOff()
    return True


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
