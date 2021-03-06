#!/opt/usr/bin/python

import subprocess
import json
import datetime
from flask import Flask, request, render_template

with open('/jffs/digipass.json', 'r') as jsonFile:
    credentials = json.loads(jsonFile.read())
    device = "https://api.particle.io/v1/devices/" + credentials['device'] + "/fire"
    token = "access_token=" + credentials['token']
    pin = credentials['pin']

curlList = ["curl", "--capath", "/opt/etc/ssl/certs/", device, "-d", token, "-d"]

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

    host = request.remote_addr
    if host in jsonData['IPs']:
        count = jsonData['IPs'][host]
        count += 1
        jsonData['IPs'][host] = count
    else:
        jsonData['IPs'][host] = 1
    num = 0
    for uniq in jsonData['IPs']:
        num += jsonData['IPs'][uniq]
    uniques = len(jsonData['IPs'])
    passOutput = "Please enter PIN"
    fireOutput = "Control the fire!"
    if request.method == 'POST':
        fireResp = "unset"
        if "fireState" in request.form:
            fireResp = request.form['fireState']
        tubResp = request.form['tubDate']
        pinIn = request.form['pin']
        if pinIn == pin:
            passOutput = "You did it!"
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
            passOutput = "Incorrect PIN"

    tubDate = datetime.datetime.strptime(jsonData['tubChange'], "%m/%d/%Y")
    now = datetime.datetime.now()
    daysSince = (now - tubDate).days

    with open('/jffs/digihouse.json', 'w') as jsonFile:
        jsonFile.write(json.dumps(jsonData, sort_keys=True, indent=4))

    return render_template('index.html', count=str(num), fireOut=fireOutput, tubOut=daysSince, \
                            tubDate=jsonData['tubChange'], passOut=passOutput, uniqOut=uniques)

if __name__ == "__main__":
    app.run()
