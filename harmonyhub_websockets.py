# -*- coding: utf-8 -*-

from time import sleep
import websocket
from websocket import create_connection

# NOTE: 18322921 is an example of what your hubId might look like
# NOTE: 57216229 is the deviceId found in the harmony conf (HASS) for the device you are controlling

# The code opens a connection locally via websockets to the hub and sends commands and status info
#
# In this case, command is PowerOn and status is 'press', 'hold', and 'release'
# It runs a lopp for the 'hold' status to blast enough IR for the candles to turn on
# (PowerOn was one of the listed commands from my harmony conf file)
#
# This was just a quick POC to verify the ability to talk to the hub
# needs a lot of work. But the reason it came about was due to Home Assistant not
# able to have the hub blast IR in a similar way 
# Other items such as the 'id' and timestamp do not seem to matter how they are set

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
