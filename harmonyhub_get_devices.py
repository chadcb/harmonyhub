# -*- coding: utf-8 -*-

from time import sleep
import json
import websocket
from websocket import create_connection

# NOTE: FIND / REPLACE THE FOLLOWING
# YOUR_HUB_IP = IP of Hub
# YOUR_HUB_ID = ID of Hub
hub_ip = 'YOUR_HUB_IP'
hub_port = '8088'
hub_id = 'YOUR_HUB_ID'

#websocket.enableTrace(True)
ws = create_connection('ws://' + hub_ip + ':' + hub_port + '/?domain=svcs.myharmony.com&hubId=' + hub_id)

ws.send(r'{"hubId":"YOUR_HUB_ID","timeout":30,"hbus":{"cmd":"vnd.logitech.connect\/vnd.logitech.deviceinfo?get","id":"0","params":{"verb":"get"}}}')
ws_data = ws.recv()
#print(ws_data)

ws.send(r'{"hubId":"YOUR_HUB_ID","timeout":30,"hbus":{"cmd":"vnd.logitech.connect\/vnd.logitech.statedigest?get","id":"0","params":{"verb":"get","format":"json"}}}')
ws_data = ws.recv()
#print(ws_data)

ws.send(r'{"hubId":"YOUR_HUB_ID","timeout":60,"hbus":{"cmd":"vnd.logitech.harmony\/vnd.logitech.harmony.engine?config","id":"0","params":{"verb":"get"}}}')
ws_data = ws.recv()
#print(ws_data)

hub_data = json.loads(ws_data)

for item in hub_data['data']['device']:
    print(item['label'])
    print(item['id'])
    for c in item['controlGroup']:
        print(c['name'])
        for f in c['function']:
            print(f)
