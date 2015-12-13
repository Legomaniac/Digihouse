#!/opt/usr/bin/python

import subprocess
import json
import datetime
from flask import Flask, request, render_template

curlList = ["curl", "--capath", "/opt/etc/ssl/certs/", "https://api.particle.io/v1/devices/230025001247343339383037/fire", "-d", "access_token=78cbc2588e09ca1aab0a3338511da8a3c0f7d736", "-d"]

def controlFire(fire):
    if fire:
        apiResp = subprocess.check_output(curlList + ["params=on"])
    else:
        apiResp = subprocess.check_output(curlList + ["params=off"])

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    with open('/jffs/digihouse.json', 'r') as jsonFile:
        jsonData = json.loads(jsonFile.read())

    fireOutput = "Control the fire!"
    if request.method == 'POST':
        fireResp = "unset"
        if "fireState" in request.form:
            fireResp = request.form['fireState']
        tubResp = request.form['tubDate']
        pinIn = request.form['pin']
        if pinIn == "haha.. not so fast!":
            if tubResp != "":
                jsonData['tubChange'] = tubResp
            if fireResp == "on":
                fireOutput = "Fire is on!"
                controlFire(True)
            elif fireResp == "off":
                fireOutput = "Fire is off!"
                controlFire(False)
            else:
                fireOutput = "Control the fire!"
        else:
            output = "Incorrect PIN"

    tubDate = datetime.datetime.strptime(jsonData['tubChange'], "%m/%d/%Y")
    now = datetime.datetime.now()
    daysSince = (now - tubDate).days

    num = jsonData['count']
    num += 1
    jsonData['count'] = num

    with open('/jffs/digihouse.json', 'w') as jsonFile:
        jsonFile.write(json.dumps(jsonData, sort_keys=True, indent=4))

    return render_template('index.html', count=str(num), fireOut=fireOutput, tubOut=daysSince) 

if __name__ == "__main__":
    app.run()
