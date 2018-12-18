# -*- coding: utf-8 -*-

from time import sleep
import json
import requests
import websocket
from websocket import create_connection

# Should only need to set the IP to your hubs address
hub_ip = '192.168.5.10'
hub_port = '8088'
hub_id = ''

# POST capture via Wireshark.
# This is from manually connecting to hub via iOS app
# ie, manually enter hub IP Address
#
#POST / HTTP/1.1
#Host: 192.168.5.20:8088
#Origin: http//:localhost.nebula.myharmony.com
#Accept-Charset: utf-8
#Content-Type: application/json
#Content-Length: 56
#Connection: keep-alive
#Accept: application/json
#User-Agent: Harmony_iOS_5.5_16
#Referer: http//:localhost.nebula.myharmony.com/mobile-fat.html
#Accept-Language: en-us
#Accept-Encoding: gzip, deflate


# Get hub id
# Probably need to add all headers, but just for testing...
#
# Not sure what the id is for in the request. My assumption is to identify the responses as they include it also
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Origin': 'http//:localhost.nebula.myharmony.com'}
r = requests.post('http://' + hub_ip + ':' + hub_port, json={"id": 124, "cmd": "connect.discoveryinfo?get", "params": {}}, headers=headers)
hub_data = json.loads(r.text)

hub_id = hub_data['data']['remoteId']

# Now connect to hub via websockets and get devices, activities, etc..
#websocket.enableTrace(True)
ws = create_connection('ws://' + hub_ip + ':' + hub_port + '/?domain=svcs.myharmony.com&hubId=' + hub_id)

hub_request = json.loads(r'{"hubId":"","timeout":30,"hbus":{"cmd":"vnd.logitech.connect\/vnd.logitech.deviceinfo?get","id":"0","params":{"verb":"get"}}}')
hub_request['hubId'] = hub_id
ws.send(json.dumps(hub_request))
ws_data = ws.recv()

hub_request = json.loads(r'{"hubId":"","timeout":30,"hbus":{"cmd":"vnd.logitech.connect\/vnd.logitech.statedigest?get","id":"0","params":{"verb":"get","format":"json"}}}')
hub_request['hubId'] = hub_id
ws.send(json.dumps(hub_request))
ws_data = ws.recv()

hub_request = json.loads(r'{"hubId":"","timeout":60,"hbus":{"cmd":"vnd.logitech.harmony\/vnd.logitech.harmony.engine?config","id":"0","params":{"verb":"get"}}}')
hub_request['hubId'] = hub_id
ws.send(json.dumps(hub_request))
ws_data = ws.recv()

hub_data = json.loads(ws_data)

#print(json.dumps(hub_data, indent=4))

# Print out a few things
for item in hub_data['data']['device']:
    print(item['label'])
    print(item['id'])
    for c in item['controlGroup']:
        print(c['name'])
        for f in c['function']:
            print(f)
