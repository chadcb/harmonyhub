# Quick hack to turn on LED candles by blasting them with IR
# I run this from within Home Assistant. I have a second script
# that does the same, but sends PowerOff commands to turn off the candles.
from time import sleep
import websocket
from websocket import create_connection


# NOTE: 18322921 is an example of what your hubId might look like
# NOTE: 57216229 is the deviceId found in the harmony conf for the device you are controlling
#
# 192.168.2.3 is an example of your local hub IP
# Default port is 8088/tcp
#
# The code opens a websockets connection to the hub, and in the example here, sends a PRESS for PowerOn.
# Next, runs a loop to blast the HOLD status for PowerOn action (ensures the candles turn on)
# Finally, sends the RELEASE status.
#
# This mimics what occurs when you hold down a button within the iOS app and allows the candles
# to turn on. I was not able to have sucess using the Home Assistant Harmony add on for this.
# It would not send repeated commands fast enough. Visually, you can see a difference at the rate
# of IR being blasted by the green light on the hub.
#
# Using iOS and Wireshark, you can capture all of the Web socket activity to see everything that is supported.
# In recent light of Harmony disabling their local api, Websockets may be an alternative way to achieve the
# same results. Wireshark provides all of the information on how to request activities from the hub along
# with deviceId's and other useful information. I haven't tested sending activity commands yet, but I expect
# it should work the same.

# PowerOn was one of the listed commands from my harmony conf file

websocket.enableTrace(True)
ws = create_connection("ws://192.168.2.3:8088/?domain=svcs.myharmony.com&hubId=18322921")


max_holds = 10
count = 0

# Send the PowerOn button a 'press'
ws.send(r'{"hubId":"18322921","timeout":30,"hbus":' \
	    r'{"cmd":"vnd.logitech.harmony\/vnd.logitech.harmony.engine?holdAction",' \
	    r'"id":"1537395108","params":{"status":"press","timestamp":"0","verb":"render",' \
	    r'"action":"{\"command\":\"PowerOn\",\"type\":\"IRCommand\",\"deviceId\":\"57216229\"}"}}}')
sleep(.002)

# Send the PowerOn button a 'hold'
while count < max_holds:
	ws.send(r'{"hubId":"18322921","timeout":30,"hbus":' \
		    r'{"cmd":"vnd.logitech.harmony\/vnd.logitech.harmony.engine?holdAction","id":"1022244803",' \
		    r'"params":{"status":"hold","timestamp":"201","verb":"render","action":' \
		    r'"{\"command\":\"PowerOn\",\"type\":\"IRCommand\",\"deviceId\":\"57216229\"}"}}}')
	sleep(.002)
	count += 1

# Send the PowerOn button a 'release'
ws.send(r'{"hubId":"18322921","timeout":30,"hbus":' \
	    r'{"cmd":"vnd.logitech.harmony\/vnd.logitech.harmony.engine?holdAction",' \
	    r'"id":"858970808","params":{"status":"release","timestamp":"659","verb":"render",' \
	    r'"action":"{\"command\":\"PowerOn\",\"type\":\"IRCommand\",\"deviceId\":\"57216229\"}"}}}')
